# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Ong Zi Liang

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """

    if nucleotide == 'A':
        return 'T'
    if nucleotide == 'C':
        return 'G'
    if nucleotide == 'T':
        return 'A'
    if nucleotide == 'G':
        return 'C'


def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
    sequence
    
    dna: a DNA sequence represented as a string
    returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    i = 0
    j = len(dna)
    data = ""
    temp = ""

    while i < j:
        temp += get_complement(dna[i])
        i += 1
    i = 0
    while j > 0:
        i += 1
        data += temp[j-1]
        j -= 1
    return data


def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    """
    j = len(dna)/3
    i = 0
    stop_condon = ''
    data = ''
    while (1):
        stop_condon = dna[i*3:3*i+3]
        if (stop_condon == 'TAG' or stop_condon == 'TAA' or stop_condon == 'TGA'):
            break
        data += stop_condon
        i += 1
        if(i > j):
            return dna
    return data

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']

    >>> find_all_ORFs_oneframe("ATGAGATGTGAACATTAGATGCCGTG")
    ['ATGAGATGTGAACAT', 'ATGCCGTG']
    """
    start_condon = ''
    i = 0
    data = []
    j = len(dna)/3
    while(i<j):
        start_condon = dna[i*3:3*i+3]
        if start_condon == 'ATG':
            data.append(rest_of_ORF(dna[3*i:]))
            k = len(rest_of_ORF(dna))/3
            i += k
        i += 1
    return data

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """

    data = []
    data += find_all_ORFs_oneframe(dna)
    data += find_all_ORFs_oneframe(dna[1:])
    data += find_all_ORFs_oneframe(dna[2:])

    return data

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    data = []
    data += find_all_ORFs(dna)
    temp = get_reverse_complement(dna)
    data += find_all_ORFs(temp)

    return data

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    i = 0
    y = 0
    temp = ""
    data = find_all_ORFs_both_strands(dna)
    for i in range(len(data)):
        if len(data[i]) > y:
            temp = data[i]
            y = len(data[i]) 
    return temp

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    i = 1
    y = 0
    temp = ""
    data = []
    for i in range(num_trials):
        temp = shuffle_string(dna)
        data.append(longest_ORF(temp))
    temp = ""
    for i in range(len(data)):
        if len(data[i]) > y:
            temp = data[i]
            y = len(data[i]) 
    return len(temp)

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    s = ""
    i = 1
    for i in range(len(dna)/3):
        s += aa_table[dna[i*3:3*i+3]]
    return s
    pass

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """
    temp = []
    data = []
    i = 0
    y = find_all_ORFs_both_strands(dna)
    for i in range(len(y)):
        if len(y[i]) > threshold:
            temp.append(y[i])
    for i in range(len(temp)):
            data.append(coding_strand_to_AA(temp[i]))
    return data
    pass

dna = load_seq("./data/X73525.fa")
print gene_finder(dna, longest_ORF_noncoding(dna, 1500))

if __name__ == "__main__":
    import doctest
    doctest.testmod()