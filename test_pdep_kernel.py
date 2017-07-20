import unittest
from pablo import swizzle, apply_pdep

class TestPDEPKernel(unittest.TestCase):
    """ 
    Hard-coded inputs and expected outputs are taken directly from the values given to and
    returned from the Parabix PDEP kernel.

    The kernel accepts swizzled input, processes the swizzles, and outputs swizzled streams.
    The Python analog accepts unswizzled input, applies PDEP to each stream, and returns the result. The
    result is then swizzled and compared to the output of the kernel.
    """
    def format_values(self, console_output, num_input_blocks):
        """
        Takes a string copied from the kernel's console output and converts it to a format
        that the testing functions can work with.

        Args:
            console_output (str): The kernel prints hex dumps of each input block, the pdep marker stream
            block, and the output blocks. console_output is created by copy/pasting that output. 
            
            E.g.
            source block                             = 00 00 00 00 00 01 20 88 04 48 10 81 12 10 80 80 82 20 41 22 04 08 10 21 10 81 02 88 10 20 40 11
            source block                             = 00 00 00 00 00 00 d0 44 00 00 00 00 01 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 20 00
            source block                             = 00 00 00 00 00 00 00 00 02 24 08 40 88 08 40 40 41 10 20 90 02 04 08 10 88 40 81 44 08 10 00 08
            source block                             = ff ff ff ff ff ff ff ff fd db f7 bf 77 f7 bf bf be ef df 6f fd fb f7 ef 77 bf 7e bb f7 ef ff f7
            PDEP_ms_blk                              = 1f ff ff ff ff f8 00 00 00 00 00 00 00 00 00 00 00 00 02 00 04 00 00 40 00 04 08 08 00 00 00 40
            result_swizzle                           = 00 00 08 08 00 00 00 40 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40
            result_swizzle                           = 00 00 02 00 04 00 00 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40
            result_swizzle                           = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
            result_swizzle                           = 17 eb bf 7e ff f8 00 00 08 14 40 81 00 00 00 00 00 00 00 00 02 00 00 00 10 28 81 02 04 00 00 00,
        
            num_input_blocks (int): The number of input/output blocks. In the example provided above num_input_blocks is 4.
        """
        lines = console_output.replace(' ', '')
        lines = lines.split('\n')
        for i in range(len(lines)):
            lines[i] = lines[i].split('=')[-1] # take everything after the '='

        input_blocks = lines[0:num_input_blocks]
        input_blocks = [int(x, 16) for x in input_blocks] # convert from string to int
        pdep_ms_block = lines[num_input_blocks:num_input_blocks+1]
        pdep_ms_block = int(pdep_ms_block[0], 16)
        output_blocks = lines[num_input_blocks+1:]
        output_blocks = [int(x, 16) for x in output_blocks]
        output_blocks = output_blocks[::-1] # for some reason the Python/Parabix order is opposite. Reverse expected output
        
        return(input_blocks, pdep_ms_block, output_blocks)

    def test_wctest(self):
        """
        Verifies the behaviour of the Parabix PDEP kernel when the pdep kernel pipeline
        is passed wctest.txt as input.
        """
        input_streams, pdep_ms, expected_output = self.format_values(
        """source block                             = 00 00 00 00 00 01 20 88 04 48 10 81 12 10 80 80 82 20 41 22 04 08 10 21 10 81 02 88 10 20 40 11
        source block                             = 00 00 00 00 00 00 d0 44 00 00 00 00 01 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 20 00
        source block                             = 00 00 00 00 00 00 00 00 02 24 08 40 88 08 40 40 41 10 20 90 02 04 08 10 88 40 81 44 08 10 00 08
        source block                             = ff ff ff ff ff ff ff ff fd db f7 bf 77 f7 bf bf be ef df 6f fd fb f7 ef 77 bf 7e bb f7 ef ff f7
        PDEP_ms_blk                              = 1f ff ff ff ff f8 00 00 00 00 00 00 00 00 00 00 00 00 02 00 04 00 00 40 00 04 08 08 00 00 00 40
        result_swizzle                           = 00 00 08 08 00 00 00 40 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40
        result_swizzle                           = 00 00 02 00 04 00 00 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40
        result_swizzle                           = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        result_swizzle                           = 17 eb bf 7e ff f8 00 00 08 14 40 81 00 00 00 00 00 00 00 00 02 00 00 00 10 28 81 02 04 00 00 00""",
        4)

        num_input_streams = len(input_streams)
        output_streams = [0] * num_input_streams
        for i in range(num_input_streams):
            apply_pdep(output_streams, i, pdep_ms, input_streams[i])
        swizzled_results = swizzle(output_streams, num_input_streams)
        self.assertEqual(expected_output, swizzled_results)

    def test_pdeptest(self):
        """ 
        Verifies the behaviour of the Parabix PDEP kernel when the pdep kernel pipeline
        is passed pdeptest.txt as input.
        """
        input_streams, pdep_ms, expected_output = self.format_values(
        """source block                             = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 00 10 08 02 00 20 09 00 84 04 42 08 51
        source block                             = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40 00 01 00 20
        source block                             = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40 00 08 04 01 00 10 04 80 02 02 20 04 08
        source block                             = ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff bf ff f7 fb fe ff ef fb 7f fd fd df fb f7
        PDEP_ms_blk                              = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 10 00 00 00
        result_swizzle                           = 00 00 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 10 00 00 00
        result_swizzle                           = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        result_swizzle                           = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        result_swizzle                           = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00""", 
        4)

        num_input_streams = len(input_streams)
        output_streams = [0] * num_input_streams
        for i in range(num_input_streams):
            apply_pdep(output_streams, i, pdep_ms, input_streams[i])
        swizzled_results = swizzle(output_streams, num_input_streams)
        self.assertEqual(expected_output, swizzled_results)

if __name__ == '__main__':
    t = TestPDEPKernel()
    TestPDEPKernel.test_wctest(t)
