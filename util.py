def containsAll(string1, string2): #longer string is string1
    a = sorted(string1) # this is just an array of single-char strings like ['e', 'h', 'l', 'l', 'o']
    b = sorted(string2) # also it's likely you can pre-sort most
    ai = 0
    bi = 0
    while ai < len(a) and bi < len(b):
      if a[ai] == b[bi]:
        ai += 1
        bi += 1
      elif a[ai] < b[bi]:
        ai += 1 # a can be longer
      else:
        return False # b cannot be longer
    if bi < len(b):
      return False # something extra in b
    return True
