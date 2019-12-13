import re

if __name__ == '__main__':
    url = 'https://img3.autoimg.cn/pano/g16/M0D/CD/67/240x180_autohomecar__wKjBx1n8FyaAU0yCAAK0rtZi_to725.jpg'
    pattern = r'https:.+/(.*?)auto.+'
    # res = re.findall(pattern=pattern,string=url)
    url = url.replace(re.findall(pattern=pattern,string=url)[0],'')
    print(url)