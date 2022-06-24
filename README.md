﻿# RBtreeManim

這個專案使用 Manim 實作 RBtree 的視覺化呈現，主要呈現 RBtree 在經過 insert 和 delete 操作後所發生的結構變化。

視覺化參考對象：
https://www.cs.usfca.edu/~galles/visualization/RedBlack.html

### Manim

Manim 是一個由 Standford 大學的大神 Grant Sanderson 所開發的動畫渲染引擎，並且 Grant Sanderson 將這套引擎使用在他的 Youtube 數學教學頻道上（https://www.youtube.com/c/3blue1brown ），Manim 主要的優點是能夠使用 python 將動畫渲染出來，使得動畫變得可程式化，且因為程式可精確的描述每個動畫物件的位置和各項資訊，所以 Manim 特別適合用作數學教學以及資料結構圖像化等精確性要求比較高的動畫。

目前在網路上有三個常用的 Manim 版本，分別由不同的社群或是由 Grant Sanderson 本人所維護：

* manimCairo
    - 最早 Grant Sanderson 所使用的版本，但該版本已經在 2020/11 停止維護。

* manimGL
    - 目前 Grant Sanderson 所維護的版本，也是現在 https://www.youtube.com/c/3blue1brown 主要使用的版本。
    - github:  https://github.com/3b1b/manim

* manimCE
    - 是 2020 年由另外一個社群 fork 出來的版本，因為由更多人維護，社群也很活躍，所以穩定性更高，也是本專案主要使用的版本。
    - github:  https://github.com/ManimCommunity/manim/
    - documentation:  https://docs.manim.community/en/stable/
    - discord:  https://discord.com/invite/mMRrZQW

### Quickstart

若要能夠完整使用 Manim，需要安裝相關的依賴套件，像是 Cairo, Pango, FFmpeg 和 LaTex，所以比較快速且不會出現環境問題的方式是使用 docker container，docker 的安裝教學在網路上已經有很多資料了，所以這邊就不再贅述。

確保系統有安裝 docker 並能正常使用後，可以直接打以下指令，記得 `{你的RBTtreeManim程式碼路徑}` 這邊要改成自己的路徑：

```
git clone git@github.com:shnovaj30101/RBtreeManim.git
cd RBtreeManim/
docker run --rm -it -v "{你的RBTtreeManim程式碼路徑}:/manim" manimcommunity/manim manim -qm main.py
```

程式跑完後會出現 `media/` 資料夾，進去 `media/videos/main/720p30`，就可以看到產生出來的 mp4 影片檔了，其中該影片檔的紅黑樹操作順序請見 `RBtreeManim/main.py` 裡面的 `RBTreeDemo.contruct` 程式內容。 

### Installation

如果要完整安裝 Manim，可以參考官方文件：  
https://docs.manim.community/en/stable/installation.html

### 動畫 Demo

![demo](https://user-images.githubusercontent.com/12492724/175510723-3f9c174e-bcdd-4bbf-b414-8eb9b9d33988.gif)

### 參數設定


