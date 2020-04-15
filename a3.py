"""
Functions for Assignment A3

This file contains the functions for the assignment. You should replace the
stubs with your own implementations.

Brandon Nathasingh bn243, Taerim Oem te89
10/11/19
"""
import introcs
import math


def complement_rgb(rgb):
    """
    Returns the complement of color rgb.

    Parameter rgb: the color to complement
    Precondition: rgb is an RGB object
    """
    # THIS IS WRONG.  FIX IT
    assert (type(rgb) == introcs.RGB),  rgb +' is not a RGB object'
    r = rgb.red; g = rgb.green; b = rgb.blue
    r = 255 - r; g = 255 - g; b = 255 - b
    rgb.red = r; rgb.green = g; rgb.blue = b
    return introcs.RGB(rgb.red, rgb.green, rgb.blue)


def str5(value):
    """
    Returns value as a string, but expanded or rounded to be exactly 5
    characters.

    The decimal point counts as one of the five characters.

    Examples:
        str5(1.3546)  is  '1.355'.
        str5(21.9954) is  '22.00'.
        str5(21.994)  is  '21.99'.
        str5(130.59)  is  '130.6'.
        str5(130.54)  is  '130.5'.
        str5(1)       is  '1.000'.

    Parameter value: the number to conver to a 5 character string.
    Precondition: value is a number (int or float), 0 <= value <= 360.
    """
    # Remember that the rounding takes place at a different place depending
    # on how big value is. Look at the examples in the specification.
    assert (type(value) ==  float or int), value + ' is not a float or int.'
    assert (value >= 0 and value <= 360), value + ' is out of range.'
    temp = str(value)
    if (type(value) == float):
        if (len(temp) >= 5):
            value = round(value,5 - temp.index('.')-1)
            temp2 = str(value)+'000'
            value = temp2[:5]
        else:
            addzeros = temp + '00000000'
            value = addzeros[:5]
    if (type(value) == int):
        addzeros = temp +'.000000'
        value = addzeros[:5]
    return str(value)


def str5_cmyk(cmyk):
    """
    Returns the string representation of cmyk in the form "(C, M, Y, K)".

    In the output, each of C, M, Y, and K should be exactly 5 characters long.
    Hence the output of this function is not the same as str(cmyk)

    Example: if str(cmyk) is

          '(0.0,31.3725490196,31.3725490196,0.0)'

    then str5_cmyk(cmyk) is '(0.000, 31.37, 31.37, 0.000)'. Note the spaces
    after the commas. These must be there.

    Parameter cmyk: the color to convert to a string
    Precondition: cmyk is an CMYK object.
    """
    assert (type(cmyk) == introcs.CMYK), cmyk+' is not a CMYK object.'
    cmyk = '('+str5(cmyk.cyan)+', '+str5(cmyk.magenta)+', ' +\
    str5(cmyk.yellow)+', ' + str5(cmyk.black)+')'
    return cmyk


def str5_hsv(hsv):
    """
    Returns the string representation of hsv in the form "(H, S, V)".

    In the output, each of H, S, and V should be exactly 5 characters long.
    Hence the output of this function is not the same as str(hsv)

    Example: if str(hsv) is

          '(0.0,0.313725490196,1.0)'

    then str5_hsv(hsv) is '(0.000, 0.314, 1.000)'. Note the spaces after the
    commas. These must be there.

    Parameter hsv: the color to convert to a string
    Precondition: hsv is an HSV object.
    """
    assert (type(hsv) == introcs.HSV), hsv+' is not an HSV object'
    hsv = '('+str5(hsv.hue)+', '+str5(hsv.saturation)+', ' +\
    str5(hsv.value)+')'
    return hsv


def rgb_to_cmyk(rgb):
    """
    Returns a CMYK object equivalent to rgb, with the most black possible.

    Formulae from https://www.rapidtables.com/convert/color/rgb-to-cmyk.html

    Parameter rgb: the color to convert to a CMYK object
    Precondition: rgb is an RGB object
    """
    assert (type(rgb) == introcs.RGB),  rgb +' is not a RGB object'
    # The RGB numbers are in the range 0..255.
    # Change them to the range 0..1 by dividing them by 255.0.
    red = rgb.red / 255.0
    green = rgb.green /255.0
    blue = rgb.blue /255.0
    black = 1-max(red,green,blue)
    if (black == 1):
        cyan = 0.0
        magenta = 0.0
        yellow = 0.0
    else:
        cyan = (1-red-black)/(1-black)*100.0
        magenta = (1-green-black)/(1-black)*100.0
        yellow = (1-blue-black)/(1-black)*100.0
    black *= 100.0
    return introcs.CMYK(cyan, magenta, yellow, black)


def cmyk_to_rgb(cmyk):
    """
    Returns : color CMYK in space RGB.

    Formulae from en.wikipedia.org/wiki/CMYK_color_model.

    Parameter cmyk: the color to convert to a RGB object
    Precondition: cmyk is an CMYK object.
    """
    assert (type(cmyk) == introcs.CMYK), cmyk+' is not an CMYK object'
    # The CMYK numbers are in the range 0.0..100.0.
    # Deal with them the same way as the RGB numbers in rgb_to_cmyk()
    cyan = cmyk.cyan / 100.0
    magenta = cmyk.magenta / 100.0
    yellow = cmyk.yellow / 100.0
    black = cmyk.black / 100.0
    red = round((1-cyan)*(1-black)*255)
    green = round((1-magenta)*(1-black)*255)
    blue = round((1-yellow)*(1-black)*255)
    return introcs.RGB(red, green, blue)


def rgb_to_hsv(rgb):
    """
    Return an HSV object equivalent to rgb

    Formulae from https://en.wikipedia.org/wiki/HSL_and_HSV

    Parameter hsv: the color to convert to a HSV object
    Precondition: rgb is an RGB object
    """
    assert (type(rgb) == introcs.RGB),  rgb +' is not a RGB object'
    # The RGB numbers are in the range 0..255.
    # Change them to range 0..1 by dividing them by 255.0.
    red = rgb.red/255.0
    green = rgb.green/255.0
    blue = rgb.blue/255.0
    maximum = max(red,green,blue)
    minimum = min(red,green,blue)
    if maximum == minimum:
        hue = 0.0
    elif maximum == red and green >= blue:
        hue = 60.0*(green-blue)/(maximum-minimum)
    elif maximum  == red and green < blue:
        hue = 60.0*(green-blue)/(maximum-minimum)+360.0
    elif maximum == green:
        hue = 60.0*(blue-red)/(maximum-minimum)+120.0
    else:
        hue = 60.0*(red-green)/(maximum-minimum)+240.0
    if maximum == 0:
        saturation = 0
    else:
        saturation = 1-minimum/maximum
    value = maximum
    return introcs.HSV(hue,saturation,value)


def hsv_to_rgb(hsv):
    """
    Returns an RGB object equivalent to hsv

    Formulae from https://en.wikipedia.org/wiki/HSL_and_HSV

    Parameter hsv: the color to convert to a RGB object
    Precondition: hsv is an HSV object.
    """
    assert (type(hsv) == introcs.HSV),  hsv +' is not a RGB object'
    hi = math.floor(hsv.hue/60)
    f = hsv.hue/60-hi
    p = hsv.value*(1-hsv.saturation)
    q = hsv.value*(1-f*hsv.saturation)
    t = hsv.value*(1-(1-f)*hsv.saturation)
    if hi == 0:
      red = hsv.value
      green = t
      blue = p
    elif hi == 1:
      red = q
      green = hsv.value
      blue = p
    elif hi == 2:
      red = p
      green = hsv.value
      blue = t
    elif hi == 3:
      red = p
      green = q
      blue = hsv.value
    elif hi == 4:
      red = t
      green = p
      blue = hsv.value
    elif hi == 5:
      red = hsv.value
      green = p
      blue = q
    return introcs.RGB(round(red*255),round(green*255),round(blue*255))


def contrast_value(value,contrast):
    """
    Returns value adjusted to the "sawtooth curve" for the given contrast

    At contrast = 0, the curve is the normal line y = x, so value is
    unaffected. If contrast < 0, values are pulled closer together, with all
    values collapsing to 0.5 when contrast = -1.  If contrast > 0, values are
    pulled farther apart, with all values becoming 0 or 1 when contrast = 1.

    Parameter value: the value to adjust
    Precondition: value is a float in 0..1

    Parameter contrast: the contrast amount (0 is no contrast)
    Precondition: contrast is a float in -1..1
    """
    assert (type(value) == float), value + ' is not a float.'
    assert (value >= 0 and value <= 1), value+' is not between 0 and 1'
    assert (type(contrast) == float), contrast + ' is not a float.'
    assert (contrast>=-1 and contrast<=1), contrast+' is not between -1 and 1'
    x = value
    c = contrast
    if c >= -1 and c < 1:
        if x< 0.25+0.25*c:
            y= ((1-c)/(1+c))*x
        elif x>0.75-0.25*c:
            y= (((1-c)/(1+c))*(x-((3-c)/4)))+((3+c)/4)
        else:
            y= (((1+c)/(1-c))*(x-((1+c)/4)))+((1-c)/4)
    elif c==1:
        if x>=0.5:
            y=1
        else:
            y=0
    return y


def contrast_rgb(rgb,contrast):
    """
    Applies the given contrast to the RGB object rgb

    This function is a PROCEDURE.  It modifies rgb and has no return value.
    It should apply contrast_value to the red, blue, and green values.

    Parameter rgb: the color to adjust
    Precondition: rgb is an RGB object

    Parameter contrast: the contrast amount (0 is no contrast)
    Precondition: contrast is a float in -1..1
    """
    assert (type(rgb) == introcs.RGB),  rgb +'is not a RGB object'
    assert (type(contrast) ==  float), contrast + ' is not a float.'
    assert (contrast >= -1 and contrast <= 1), contrast+\
    ' is not between -1 and 1'
    red = rgb.red/255.0
    green = rgb.green /255.0
    blue = rgb.blue /255.0
    rgb.red = round(contrast_value(red,contrast)*255)
    rgb.green = round(contrast_value(green,contrast)*255)
    rgb.blue = round(contrast_value(blue,contrast)*255)
