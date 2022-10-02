
a text readability algorithm on the Chinese texts for children's recognizing characters and learning to read.

儿童识字用汉语文本的难度算法。

## 思路

主要测算识读难度，而不是理解难度。

因而主要依赖[字频表](https://blog.xiiigame.com/2020-06-24-%E8%87%AA%E5%88%B6%E5%84%BF%E7%AB%A5%E5%90%AF%E8%92%99%E9%9B%86%E4%B8%AD%E8%AF%86%E5%AD%97%E8%AF%AD%E6%96%99%E5%BA%93%E4%B8%8E%E5%88%86%E7%BA%A7%E5%AD%97%E8%A1%A8/)，以及对识字过程的经验与先验假设（调参和实测验证）。详见代码注释。

实际上没有做多少调参与验证工作，效果还不错。

## 参考

* [Readability, or textual difficulty](https://simple.wikipedia.org/wiki/Readability)
* [List of readability tests](https://simple.wikipedia.org/wiki/List_of_readability_tests)
* [How Long Does It Take to Remember a Word?](https://spellquiz.com/blog/how-to-remember-the-word)
    * >Linguistic experts suggest that if you encounter a word 12-times through a year, your brain will store the piece of information as a long-term memory.

