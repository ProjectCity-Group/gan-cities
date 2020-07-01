def mapRangeToRange(inputNum, inputRange, outputRange):
    inputRangeVal = inputRange[1] - inputRange[0]
    outputRangeVal = outputRange[1] - outputRange[0]
    return (inputNum - inputRange[0]) / inputRangeVal * outputRangeVal + outputRange[0]

