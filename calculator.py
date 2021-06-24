import traceback


class CalculationParser:
    bodmasOrdering = ['+', '-', '*', '/', '^']
    SupportedOperationsMsg = 'Supported Operations:\n 1. Addition `+`\n 2. Subtraction `-`\n 3. Multiplication `*`\n 4. Division `/`\n'
    IncorrectOperationMsg = "Incorrect/Unrecognized operation request"
    ZeroDivisionError = "Attempt to Divide by Zero"
    userInput = ''
    specialPositions = []

    def handleCalc(self, value, sndValue, bodmasInd):
        if bodmasInd == 0:
            # add
            value += sndValue
        elif bodmasInd == 1:
            # subtract
            value -= sndValue
        elif bodmasInd == 2:
            # mult
            value *= sndValue
        elif bodmasInd == 3:
            # div
            try:
                value /= sndValue
            except ZeroDivisionError:
                print(self.ZeroDivisionError)
                print("Operation '"+self.userInput+"' is invalid\n")
                return
        return value

    def operateOnSplitList(self, splitList, bodmasInd):
        value = 0
        value = self.handleInputSplit(splitList[0], bodmasInd+1)
        if value is None:
            return None
        for i in range(1, len(splitList)):
            sndValue = self.handleInputSplit(splitList[i], bodmasInd+1)
            if sndValue is None:
                return None
            value = self.handleCalc(value, sndValue, bodmasInd)

        return value

    def checkSpecialCases(self, expr, bodmasInd):
        specialCase = False
        self.specialPositions = []
        if bodmasInd != 1:
            return False
        if expr[0] == '-':
            specialCase = True
            self.specialPositions.append(0)

        chrCount = 0
        ind = 0
        for chr in expr:
            chrCount = chrCount + 1 if not chr.isnumeric() else 0
            if chrCount > 1 and chr == '-':
                specialCase = True
                self.specialPositions.append(ind)
            ind += 1
        return specialCase

    def handleImmutableReplace(self, expr, pos, tempChar):
        return expr[:pos] + tempChar + expr[pos+1:]

    def handleMinusRepeats(self, expr):
        mult = ''
        formatExp = ''
        for ind in expr:
            if ind == '-':
                mult = '-' if mult is not '-' else ''
            else:
                formatExp += mult+ind
                mult = ''
        return formatExp

    def handleSpecialCases(self, expr):
        splitChar = '-'
        tempChar = '%'
        for ind in range(0, len(self.specialPositions)):
            specialPos = self.specialPositions[ind]
            expr = self.handleImmutableReplace(expr, specialPos, tempChar)

        splitList = expr.split(splitChar)
        for ind in range(0, len(splitList)):
            splitList[ind] = splitList[ind].replace(tempChar, splitChar)
            splitList[ind] = self.handleMinusRepeats(splitList[ind])
        return splitList

    def handleInputSplit(self, expr, bodmasInd):
        if len(expr) < 1 or bodmasInd == len(self.bodmasOrdering) or expr.isnumeric():
            try:
                return float(expr)
            except Exception as e:
                print('\n'+self.IncorrectOperationMsg)
                print("Operation '"+self.userInput+"' is not supported\n")
                return
        splitChar = self.bodmasOrdering[bodmasInd]
        if self.checkSpecialCases(expr, bodmasInd) is False:
            splitList = expr.split(splitChar)
        else:
            splitList = self.handleSpecialCases(expr)
        return self.operateOnSplitList(splitList, bodmasInd)

    def greetMessage(self):
        print('Basic Calculator')
        print(calculator.SupportedOperationsMsg)
        print('Press `q` to quit\n')

    def eventLoop(self):
        while self.userInput != 'q':
            self.greetMessage()
            self.userInput = input()
            if self.userInput == 'q':
                break
            else:
                computedVal = calculator.handleInputSplit(self.userInput, 0)
                if computedVal is not None:
                    computedVal = round(computedVal, 3)
                    print(computedVal, '\n')


calculator = CalculationParser()
calculator.eventLoop()
