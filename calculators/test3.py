import sys

listsAreFilled = True
listsAreNotEqual = False

try:
# simple version
# if listsAreFilled == False or listsAreNotEqual == True:
#            raise ValueError
#
  if listsAreFilled == False
            raise ValueError ("lists are not filled")
        if listsAreNotEqual == True :
            raise ValueError ("lists are not equal")

except ValueError:
  print 'mistake'
  sys.exit(0)

print 'get to the end'
