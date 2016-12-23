from lxml import etree
from lxml import html

# html 和etree都是解析html的库，写法不同
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
</div>

'''
html = etree.HTML(text)

result1 = html.xpath('//li/@class')
# print(result1)
# ['item-0', 'item-1', 'item-inactive', 'item-1', 'item-0']

span = html.xpath('//li/a//@href')

span1 = html.xpath('//li[last()]/a/@href')

# 显示到处第二个元素的内容
result2 = html.xpath('//li[last()-1]/a')
span2 = result2[0].text  # 没有text的话显示的地址
print(span2)
# span2 = fourth item

result3 = html.xpath('//li[last()-1]/a/@href')
print(result3)  # 通过xpath操作，生成一个list
# result3 = ['link4.html']

result4 = html.xpath('//*[@class="bold"]')
print(result4)
# span 获取 class 为 bold 的标签名