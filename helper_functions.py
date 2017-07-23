"""
Contains helper functions used in test_pdep_kernel.py
"""
from pablo import apply_pdep, swizzle

def format_values(console_output, num_input_blocks, num_block_sets=1):
        """
        Takes a string copied from the kernel's console output and converts it to a format
        that the testing functions can work with.

        Args:
            console_output (str): The kernel prints hex dumps of each input block, the pdep marker stream
            block, and the output blocks. console_output is created from that. E.g.:

            source block                             = 00 00 00 00 00 01 20 88 04 48 10 81 12 10 80 80 82 20 41 22 04 08 10 21 10 81 02 88 10 20 40 11
            source block                             = 00 00 00 00 00 00 d0 44 00 00 00 00 01 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 20 00
            source block                             = 00 00 00 00 00 00 00 00 02 24 08 40 88 08 40 40 41 10 20 90 02 04 08 10 88 40 81 44 08 10 00 08
            source block                             = ff ff ff ff ff ff ff ff fd db f7 bf 77 f7 bf bf be ef df 6f fd fb f7 ef 77 bf 7e bb f7 ef ff f7
            PDEP_ms_blk                              = 1f ff ff ff ff f8 00 00 00 00 00 00 00 00 00 00 00 00 02 00 04 00 00 40 00 04 08 08 00 00 00 40
            result_swizzle                           = 00 00 08 08 00 00 00 40 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40
            result_swizzle                           = 00 00 02 00 04 00 00 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40
            result_swizzle                           = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
            result_swizzle                           = 17 eb bf 7e ff f8 00 00 08 14 40 81 00 00 00 00 00 00 00 00 02 00 00 00 10 28 81 02 04 00 00 00,
        
            num_input_blocks (int): The number of input/output blocks. In the example provided above, num_input_blocks is 4.
            num_block_sets (int): The number of input/pdep/output sets contained in console_input. This number is equivalent to the number of blocks processed
            by the Parabix kernel.
        Returns:
            input_blocks (array of ints): input blocks in a format the Python functions accept. E.g. (in decimal format rather than hex):
            [0]:7308569839543276070860605882704647002519782667084839218520512242113021214784
            [1]:210624583337114373395836055367340864637790190801098222508621955072
            [2]:3654284919561013452093188567956487445892550468904629417868863214089089843200
            [3]:10819726235100219966738542146045191097401082953856532763855286610790526746688
            pdep_ms_block (int): pdep block ""
            output_blocks (array of ints): output blocks ""         
        """
        block_sets = []
        block_start = 0 # tracks start location of next block within console_output
        for j in range(num_block_sets):
            # strip out non-numeric characters
            lines = console_output.replace(' ', '')
            lines = lines.split('\n')
            for i in range(len(lines)):
                lines[i] = lines[i].split('=')[-1] # take everything after the '='

            # extract input, pdep, and output block data
            read_start = block_start
            read_end = block_start + num_input_blocks
            input_blocks = lines[read_start:read_end]
            input_blocks = [int(x, 16) for x in input_blocks] # convert from string to int
            read_start = read_end
            read_end = read_start + 1
            pdep_ms_block = lines[read_start:read_end]
            pdep_ms_block = int(pdep_ms_block[0], 16)
            read_start = read_end
            read_end = read_start + num_input_blocks
            output_blocks = lines[read_start:read_end]
            output_blocks = [int(x, 16) for x in output_blocks]

            block_sets.append((input_blocks, pdep_ms_block, output_blocks))
            block_start = read_end

        return block_sets

def compare_expected_actual(tester, block_sets):
    """
    For each block set, compare expected values (the output from the Python PDEP function) with the
    actual output from the Parabix PDEP function. TODO expand
    """
    for block_set in block_sets:
        input_streams, pdep_ms, expected_output = block_set # unpack tuplez
        num_input_streams = len(input_streams)
        output_streams = [0] * num_input_streams
        for i in range(num_input_streams):
            print("pdep ms")
            print(hex(pdep_ms))
            print("input_stream " + str(i))
            print(hex(input_streams[i]))
            apply_pdep(output_streams, i, pdep_ms, input_streams[i])
            print("unswizzled output " + str(i))
            print(hex(output_streams[i]))
        swizzled_results = swizzle(output_streams, num_input_streams)
        for i in range(num_input_streams):
            print("expected_output " + str(i))
            print(hex(expected_output[i]))
            print ("swizzled output " + str(i))
            print(hex(swizzled_results[i]))
        tester.assertEqual(expected_output, swizzled_results)