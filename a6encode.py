"""
Steganography methods for the imager application.

This module provides all of the test processing operations (encode, decode)
that are called by the application. Note that this class is a subclass of Filter.
This allows us to layer this functionality on top of the Instagram-filters,
providing this functionality in one application.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Brandon Nathasingh (bn243), Taerim Eom (te89)
Date:   November 20, 2019
"""
import a6filter


class Encoder(a6filter.Filter):
    """
    A class that contains a collection of image processing methods

    This class is a subclass of Filter.  That means it inherits all of the
    methods and attributes of that class too. We do that separate the
    steganography methods from the image filter methods, making the code
    easier to read.

    Both the `encode` and `decode` methods should work with the most recent
    image in the edit history.
    """

    def encode(self, text):
        """
        Returns True if it could hide the text; False otherwise.

        This method attemps to hide the given message text in the current
        image. This method first converts the text to a byte list using the
        encode() method in string to use UTF-8 representation:

            blist = list(text.encode('utf-8'))

        This allows the encode method to support all text, including emoji.

        If the text UTF-8 encoding requires more than 999999 bytes or the
        picture does  not have enough pixels to store these bytes this method
        returns False without storing the message. However, if the number of
        bytes is both less than 1000000 and less than (# pixels - 10), then
        the encoding should succeed.  So this method uses no more than 10
        pixels to store additional encoding information.

        Parameter text: a message to hide
        Precondition: text is a string
        """
        try:
            textbyte = list(text.encode('utf-8'))
            if len(textbyte) > 999999:
                return False
            self._encode_pixel(0, 123)
            self._encode_pixel(1, 234)
            self._encode_pixel(2, 345)
            length=len(textbyte)
            self._encode_pixel(3, length)
            for i in range(len(textbyte)):
                self._encode_pixel(i+4, textbyte[i])
            return True
        except:
            return False

        #adjust the encoding length because length may be too long for one pixel


        # You may modify anything in the above specification EXCEPT
        # The first line (Returns True...)
        # The last paragraph (If the text UTF-8 encoding...)
        # The precondition (text is a string)
        pass    # Implement me

    def decode(self):
        """
        Returns the secret message (a string) stored in the current image.

        The message should be decoded as a list of bytes. Assuming that a list
        blist has only bytes (ints in 0.255), you can turn it into a string
        using UTF-8 with the decode method:

            text = bytes(blist).decode('utf-8')

        If no message is detected, or if there is an error in decoding the
        message, this method returns None
        """
        pixel0= self._decode_pixel(0)
        pixel1= self._decode_pixel(1)
        pixel2= self._decode_pixel(2)
        if pixel0 != 123:
            return None
        if pixel1 != 234:
            return None
        if pixel2 != 345:
            return None
        length = self._decode_pixel(3)
        message = []
        try:
            for i in range(length):
                byte = self._decode_pixel(i+4)
                message.append(byte)
            return bytes(message).decode('utf-8')
        except:
            return None



        #why is decode not checking enough. something wrong with length
        # You may modify anything in the above specification EXCEPT
        # The first line (Returns the secret...)
        # The last paragraph (If no message is detected...)
        #how does it know how long the message is?
        pass    # Implement me

    # HELPER METHODS
    def _decode_pixel(self, pos):
        """
        Return: the number n hidden in pixel pos of the current image.

        This function assumes that the value was a 3-digit number encoded as
        the last digit in each color channel (e.g. red, green and blue).

        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        # This is helper. You do not have to use it. You are allowed to change it.
        # There are no restrictions on how you can change it.
        rgb = self.getCurrent()[pos]
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return  (red % 10) * 100  +  (green % 10) * 10  +  blue % 10

    def _encode_pixel(self, pos, code):
        """
        Encodes the given code into the pixel at the given position of the
        current Image.

        This function takes any 3-digit or less number and makes the following
        conversions:
        the ones' digit of the red byte of the pixel at the given position
        to the leading digit of the code,
        converts the ones' digit of the green byte to the second digit
        (if applicable) of the code,
        and converts the ones' digit of the blue byte to the third
        digit of the code (if applicable).

        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        rgb = self.getCurrent()[pos]
        red = (rgb[0] // 10) * 10
        green = (rgb[1] // 10) * 10
        blue = (rgb[2] // 10) * 10
        hundreds = code // 100
        tens = code // 10 % 10
        ones = code % 10
        red += hundreds
        green += tens
        blue += ones
        rgb = (red, green, blue)
        self.getCurrent()[pos] = rgb
