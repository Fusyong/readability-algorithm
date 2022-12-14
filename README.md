
a text readability algorithm on the Chinese texts for children's recognizing characters and learning to read.

儿童识字用汉语文本的难度算法。

## 思路

以儿童阅读入门兼识字为假设情境，主要估测文本的**识读难度**，而不是**理解难度**。

因而主要依赖[字频表](https://blog.xiiigame.com/2020-06-24-%E8%87%AA%E5%88%B6%E5%84%BF%E7%AB%A5%E5%90%AF%E8%92%99%E9%9B%86%E4%B8%AD%E8%AF%86%E5%AD%97%E8%AF%AD%E6%96%99%E5%BA%93%E4%B8%8E%E5%88%86%E7%BA%A7%E5%AD%97%E8%A1%A8/)，以及对识字过程的经验与先验假设（实测-调参）。详见代码注释。

输出每篇文本的5个值：字数；字种；文难度；句难度；分句难度；单字难度。如下，两首诗及其所得数值：

| 文本|字数|字种|文难度|句难度|分句难度|单字难度 |
| :-|-:|-:|-:|-:|-:|-:|
| 解落三秋叶，能开二月花。过江千尺浪，入竹万竿斜。|20| 20| 2273.82| 1136.91| 568.46| 113.69 |
| 灞原风雨定，晚见雁行频。落叶他乡树，寒灯独夜人。|20| 20| 2290.09| 1145.05| 572.52| 114.50 |

你可以使用这些值，根据实际需要构建排序算法。

实测效果还不错，目前可用于辅助文本难易排序。（实际上没有做多少实测-调参工作，也就是说，预计不会有严重的过拟合问题。）

## 参考

* [Readability, or textual difficulty](https://simple.wikipedia.org/wiki/Readability)
* [List of readability tests](https://simple.wikipedia.org/wiki/List_of_readability_tests)
* [How Long Does It Take to Remember a Word?](https://spellquiz.com/blog/how-to-remember-the-word)
    * >Linguistic experts suggest that if you encounter a word 12-times through a year, your brain will store the piece of information as a long-term memory.

