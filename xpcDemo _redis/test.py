
if __name__ == '__main__':
    values =['a','b','c',1,2,3]
    values = list(map(lambda x:x if isinstance(x,str) else None,values))
    print(values)