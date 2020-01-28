test for named entiry recognition using ginza (Japanese NLP library) version 3

# GiNZA v3.0の拡張固有表現抽出を試してみた

## 概要
はいみなさんこんにちは。こちらはYouTube動画「GiNZA v3.0の拡張固有表現抽出を試してみた 【自然言語処理】」（[https://youtu.be/bfDqnFLu7Ek](https://youtu.be/bfDqnFLu7Ek)）で使ったソースコードになります。動画の内容をテキストで読みたい方はブロマガ（[ar1859276](https://ch.nicovideo.jp/skas-web/blomaga/ar1859276)）をご覧ください。


## 注意点とか

GiNZAと同じくMITライセンスで公開しますが，ソースコードをそのまま使わないほうがいいと思います。

- コードがあまりきれいではないです。
- 良くない書き方をしているところなどコメントでコントしてたりします。


## 必要なライブラリー郡

以下のライブラリーをpipでインストールして，適切なディレクトリーにソースコードを配置すれば，おそらく動きます。ただし，入れたライブラリーをすべてメモしてたわけではないので，確証はありません。申し訳ありませんが，適宜必要なライブラリーをインストールしてください。

- django
- ginza
- mojimoji
- timeout-decorator


## リンク集

このソースコード関連のページ

- 動画：[https://youtu.be/bfDqnFLu7Ek](https://youtu.be/bfDqnFLu7Ek)
- ブロマガ：[ar1859276](https://ch.nicovideo.jp/skas-web/blomaga/ar1859276)

これ作った人の関連ページ

- YouTubeチャンネル：[https://youtube.com/c/0150159SK](https://youtube.com/c/0150159SK)
- ニコニコミュ：[co2335074](https://com.nicovideo.jp/community/co2335074)
- ブロマガ：[ar1739328](https://ch.nicovideo.jp/skas-web/blomaga/ar1739328)
- Twitter：[@SK_Animation](https://twitter.com/SK_Animation)

GiNZA関連のページ

- GiNZAのWebページ：[https://megagonlabs.github.io/ginza/](https://megagonlabs.github.io/ginza/)（「ginza nlp」で検索すると出てきます）
- GiNZAの詳しい解説：[https://www.slideshare.net/MegagonLabs/nlp2019-ginza-139011245](https://www.slideshare.net/MegagonLabs/nlp2019-ginza-139011245)
- GiNZAのGitHub：[https://github.com/megagonlabs/ginza](https://github.com/megagonlabs/ginza)

おまけ（動画中で例文として使ったもの関連）

- （DNSの更新を忘れ，そしていまだにSSL/TLS化してないことで有名な）ラブライブ！公式サイトだよ！：[http://www.lovelive-anime.jp/](http://www.lovelive-anime.jp/)
- わーすた公式Webページ：[https://wa-suta.world/](https://wa-suta.world/)
