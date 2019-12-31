import re
from scrapy import cmdline

if __name__ == "__main__":
    cmdline.execute('scrapy crawl xpc'.split(' '))
    # cates = ['\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tMV', '\n\t\t\t\t\t\t\t', '\n\t\t\t\t\t\t\t\t广告',
    #          '\n\t\t\t\t\t\t\t\t -\n\t\t\t\t\t\t\t\t', '服装配饰',
    #          '\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t', '\n\t\t\t\t\t\t\t', '\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tMV',
    #          '\n\t\t\t\t\t\t\t\t剧情短片',
    #          '\n\t\t\t\t\t\t\t\t -\n\t\t\t\t\t\t\t\t', '爱情',
    #          '\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t', '\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t', '\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t短视频']
    #

    def cate_fun(cates):
        cates = [i.strip() for i in cates]

        res = []
        for index, value in enumerate(cates):
            if not value:
                cates.pop(index)
        for i in range(len(cates) - 2):
            if re.match('\w+', cates[i]) and cates[i + 1] == '-':
                res.append(cates[i] + '-' + cates[i + 2])
                # i = i + 2
            else:
                if cates[i] != '-' and cates[i] != '' and cates[i - 1] != '-':
                    res.append(cates[i])
        res.append(cates[-1])
        return res

