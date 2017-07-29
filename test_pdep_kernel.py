"""
Contains functions to test the PDEP Parabix kernel.
"""
import unittest
import helper_functions
import pablo

class TestPDEPKernel(unittest.TestCase):
    """
    Hard-coded inputs (source block) and expected outputs (result_swizzle) are taken directly from
    the values given to and returned from the Parabix PDEP kernel.

    The kernel accepts swizzled input, processes the swizzles, and outputs swizzled streams.
    The Python analog accepts unswizzled input, applies PDEP to each stream in the input, and returns the result.
    The result is then swizzled and compared to the output of the kernel. 
    
    Source block represents unswizzled input blocks,
    result_swizzle is the swizzled results. We pass the source blocks to the Python function and compare the results
    to result_swizzle.
    """
    def test_wctest(self):
        """
        Verifies the behaviour of the Parabix PDEP kernel when the pdep kernel pipeline
        is passed wctest.txt as input.
        """
        num_block_sets = 1
        block_sets = helper_functions.format_values(
        """source block                             = 00 00 00 00 00 01 20 88 04 48 10 81 12 10 80 80 82 20 41 22 04 08 10 21 10 81 02 88 10 20 40 11
        source block                             = 00 00 00 00 00 00 d0 44 00 00 00 00 01 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 20 00
        source block                             = 00 00 00 00 00 00 00 00 02 24 08 40 88 08 40 40 41 10 20 90 02 04 08 10 88 40 81 44 08 10 00 08
        source block                             = ff ff ff ff ff ff ff ff fd db f7 bf 77 f7 bf bf be ef df 6f fd fb f7 ef 77 bf 7e bb f7 ef ff f7
        PDEP_ms_blk                              = 1f ff ff ff ff f8 00 00 00 00 00 00 00 00 00 00 00 00 02 00 04 00 00 40 00 04 08 08 00 00 00 40
        result_swizzle                           = 00 00 08 08 00 00 00 40 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40
        result_swizzle                           = 00 00 02 00 04 00 00 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40
        result_swizzle                           = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        result_swizzle                           = 17 eb bf 7e ff f8 00 00 08 14 40 81 00 00 00 00 00 00 00 00 02 00 00 00 10 28 81 02 04 00 00 00""",
        4, num_block_sets)
        
        helper_functions.compare_expected_actual(self, block_sets)

    def test_pdeptest(self):
        """
        Verifies the behaviour of the Parabix PDEP kernel when the pdep kernel pipeline
        is passed pdeptest.txt as input.
        """
        num_block_sets = 1
        block_sets = helper_functions.format_values(
        """source block                             = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 00 10 08 02 00 20 09 00 84 04 42 08 51
        source block                             = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40 00 01 00 20
        source block                             = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40 00 08 04 01 00 10 04 80 02 02 20 04 08
        source block                             = ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff bf ff f7 fb fe ff ef fb 7f fd fd df fb f7
        PDEP_ms_blk                              = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 10 00 00 00
        result_swizzle                           = 00 00 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 10 00 00 00
        result_swizzle                           = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        result_swizzle                           = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        result_swizzle                           = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00""", 
        4, num_block_sets)

        helper_functions.compare_expected_actual(self, block_sets)

    def test_unicodetest(self):
        """
        Verifies the behaviour of the Parabix PDEP kernel when the pdep kernel pipeline
        is passed unicodetest.txt as input.
        """
        num_block_sets = 19
        block_sets = helper_functions.format_values(pablo.readfile("Resources/unicodetest_output.txt"), 4, num_block_sets)

        helper_functions.compare_expected_actual(self, block_sets)

    def test_unicodetest2(self):
        """
        Verifies the behaviour of the Parabix PDEP kernel when the pdep kernel pipeline
        is passed unicodetest.txt as input. This test uses an extrememly
        dense PDEP marker stream to ensure that multiple source blocks are consumed (I went into
        wc and changed the PDEP marker stream from the character class stream for 'a' to
        the character class stream for not(space))
        """
        num_block_sets = 19
        block_sets = helper_functions.format_values(pablo.readfile("Resources/unicodetest_dense_output.txt"), 4, num_block_sets)

        helper_functions.compare_expected_actual(self, block_sets)
        
if __name__ == '__main__':
    t = TestPDEPKernel()
    TestPDEPKernel.test_unicodetest(t)
