## Project Structure ✨

<!-- START_STRUCTURE -->
```
├── Assets/
│   └── image.png
├── Backend/
│   ├── Dataset/
│   │   ├── feedback.html
│   │   ├── security.md
│   │   ├── test/
│   │   │   ├── _tokenization.txt
│   │   │   ├── cheating/
│   │   │   │   ├── cheating-26-Small-_jpg.rf.34c67be03ce190073c3a1e81c1318f43.jpg
│   │   │   │   ├── cheating-33-Small-_jpg.rf.91850d20ddcbfd8871ac1519a8390a13.jpg
│   │   │   │   ├── cheating-43-Small-_jpg.rf.4fdb9084de60efe28bda0b8de7b126e2.jpg
│   │   │   │   ├── cheating-45-Small-_jpg.rf.70635fac0066090ae285fd1a6b69ddcf.jpg
│   │   │   │   ├── cheating-5-Small-_jpg.rf.8d3d6a4e7f32046c0afe835f124c6915.jpg
│   │   │   │   ├── cheating-51-Small-_jpg.rf.5ed4a059d30770b34f0e77cc5b72a6c4.jpg
│   │   │   │   └── cheating-53-Small-_jpg.rf.af7734694d557b18815176b50bfcf614.jpg
│   │   │   └── not cheating/
│   │   │       ├── Not-Cheating-17-_jpg.rf.0b0e288c155a0455ba71546beb8e3de3.jpg
│   │   │       ├── Not-Cheating-2-_jpg.rf.b9aeefe419dd015a2754eea7638c66d0.jpg
│   │   │       ├── Not-Cheating-41-_jpg.rf.4b322d959233279c9279066ea0b77172.jpg
│   │   │       ├── Not-Cheating-47-_jpg.rf.ae22ceda1735c5f0b85085b3e3c09159.jpg
│   │   │       └── Not-Cheating-52-_jpg.rf.d81353e63275e208aa41f3a79747c0d4.jpg
│   │   ├── train/
│   │   │   ├── _tokenization.txt
│   │   │   ├── cheating/
│   │   │   │   ├── cheating-1-Small-_jpg.rf.8597318d55082957fa84b95507159e00.jpg
│   │   │   │   ├── cheating-1-Small-_jpg.rf.e4ce0d7a2e73bbba1771359329399104.jpg
│   │   │   │   ├── cheating-11-Small-_jpg.rf.31667a0b1391f6ab2442893fba4cd081.jpg
│   │   │   │   ├── cheating-11-Small-_jpg.rf.9fc5cae05d1045ffc3640a61fb1f6cb1.jpg
│   │   │   │   ├── cheating-12-Small-_jpg.rf.1e266bd240f6e104afbcc8a59d08e8d2.jpg
│   │   │   │   ├── cheating-12-Small-_jpg.rf.2c46788376437659a8c59a6536c3b3ae.jpg
│   │   │   │   ├── cheating-13-Small-_jpg.rf.2fb8953c52b5cd770e9b88f69986bcd5.jpg
│   │   │   │   ├── cheating-13-Small-_jpg.rf.ae27901414839d123c55a982b2f08ede.jpg
│   │   │   │   ├── cheating-14-Small-_jpg.rf.bac417cea7dd4d16b1537189acc15189.jpg
│   │   │   │   ├── cheating-14-Small-_jpg.rf.bdfb6f0042274a4de58dd1c5c22fcf39.jpg
│   │   │   │   ├── cheating-15-Small-_jpg.rf.1d42546e3dd047ead5133fd7dc635308.jpg
│   │   │   │   ├── cheating-15-Small-_jpg.rf.5024d6add3f3dc2bcdbe483cfe8edba6.jpg
│   │   │   │   ├── cheating-17-Small-_jpg.rf.7fd1863221b7cbc614a093e08790d235.jpg
│   │   │   │   ├── cheating-17-Small-_jpg.rf.cccb74792f79beffbfd149c1d7e26934.jpg
│   │   │   │   ├── cheating-18-Small-_jpg.rf.16103a45eed9819074f9645387c3ef1e.jpg
│   │   │   │   ├── cheating-18-Small-_jpg.rf.ce803a78483e28c295c7089b9ef51c07.jpg
│   │   │   │   ├── cheating-19-Small-_jpg.rf.44409a06d2a1c477ae411d4154a82135.jpg
│   │   │   │   ├── cheating-19-Small-_jpg.rf.abfdb8f7776e9caac28abe2ebd7594cb.jpg
│   │   │   │   ├── cheating-20-Small-_jpg.rf.3c27e52b628275c08c709e5fb062105c.jpg
│   │   │   │   ├── cheating-20-Small-_jpg.rf.cd87ad91f971057f076a784077101dae.jpg
│   │   │   │   ├── cheating-21-Small-_jpg.rf.1e18ab0642bfc0c66489bc0eff0cdb72.jpg
│   │   │   │   ├── cheating-21-Small-_jpg.rf.3faba8f8b95f339b739c53ea7c797f45.jpg
│   │   │   │   ├── cheating-22-Small-_jpg.rf.4ff48f6c22604bcb0d47e074cdaf2bab.jpg
│   │   │   │   ├── cheating-22-Small-_jpg.rf.8be98c53e2772ec3827e94fda96faecf.jpg
│   │   │   │   ├── cheating-23-Small-_jpg.rf.2317e5e5cacb5fee1c269873ab2df5f6.jpg
│   │   │   │   ├── cheating-23-Small-_jpg.rf.3effc91b2ae4ced985c66c57abee6433.jpg
│   │   │   │   ├── cheating-24-Small-_jpg.rf.342253acc6cea2fbc5aee3eeace41db2.jpg
│   │   │   │   ├── cheating-24-Small-_jpg.rf.d73d7c96d38b9c23eaf25a54371b7931.jpg
│   │   │   │   ├── cheating-25-Small-_jpg.rf.944387731f7fe559a667698de89be702.jpg
│   │   │   │   ├── cheating-25-Small-_jpg.rf.fd9778406ac8b4d36b4a86d20e159b9b.jpg
│   │   │   │   ├── cheating-28-Small-_jpg.rf.7c202db263b4ce36068fe99a153b1ace.jpg
│   │   │   │   ├── cheating-28-Small-_jpg.rf.f994f9f9dcc762f71e65b096dd3ce78d.jpg
│   │   │   │   ├── cheating-29-Small-_jpg.rf.fa7ec88db27c12b316727d2a72473ea6.jpg
│   │   │   │   ├── cheating-29-Small-_jpg.rf.fd9bc38e844f9f7f346ca51928bdba2d.jpg
│   │   │   │   ├── cheating-3-Small-_jpg.rf.213387b62ba6825550bfdcbcf02a85aa.jpg
│   │   │   │   ├── cheating-3-Small-_jpg.rf.7c0870974faee346c66f87a3b7b48cc0.jpg
│   │   │   │   ├── cheating-30-Small-_jpg.rf.e3e91bb7dabc88d0a446d2a473905ab3.jpg
│   │   │   │   ├── cheating-30-Small-_jpg.rf.eb1f2e9bb7b904064bc83438e4721fb1.jpg
│   │   │   │   ├── cheating-32-Small-_jpg.rf.234cb892e4207c642fbde3c828305fcf.jpg
│   │   │   │   ├── cheating-32-Small-_jpg.rf.7c7880864ecacf379727610b10ea69f9.jpg
│   │   │   │   ├── cheating-34-Small-_jpg.rf.aebfaa47ca0e8dbe20aa4dfc6fc22887.jpg
│   │   │   │   ├── cheating-34-Small-_jpg.rf.c00799246fb95272210da69be1284a9c.jpg
│   │   │   │   ├── cheating-36-Small-_jpg.rf.a81fd6b839a3a9811205fb96b45d7b19.jpg
│   │   │   │   ├── cheating-36-Small-_jpg.rf.f2a3f25e7ea90cce44875420e946bf83.jpg
│   │   │   │   ├── cheating-37-Small-_jpg.rf.1227c81810fad8a03f605dda84d2db55.jpg
│   │   │   │   ├── cheating-37-Small-_jpg.rf.45c410865175ad62eeb389a7f0b34c75.jpg
│   │   │   │   ├── cheating-38-Small-_jpg.rf.aaa321ea9b979eeebf1fc398182f43ab.jpg
│   │   │   │   ├── cheating-38-Small-_jpg.rf.de0732957863b09fe6aa56e13cc97f48.jpg
│   │   │   │   ├── cheating-39-Small-_jpg.rf.4712d8c2c955819e5e55164cef993a27.jpg
│   │   │   │   ├── cheating-39-Small-_jpg.rf.56d327fe4ed26c0c42359b395d633255.jpg
│   │   │   │   ├── cheating-4-Small-_jpg.rf.43c421e9db3186bb76b2f1f3c743f6ef.jpg
│   │   │   │   ├── cheating-4-Small-_jpg.rf.bdbaa14b690e8581b85b6e94e9fab1b3.jpg
│   │   │   │   ├── cheating-41-Small-_jpg.rf.9fe8e818a9ad9b682833bae0bd1c4dc4.jpg
│   │   │   │   ├── cheating-41-Small-_jpg.rf.d75119877641032edb565b86dbc61060.jpg
│   │   │   │   ├── cheating-46-Small-_jpg.rf.5ac78e9e9938c352c7896228adbe33b8.jpg
│   │   │   │   ├── cheating-46-Small-_jpg.rf.ffc802361e340e2650dd61fe05b90b17.jpg
│   │   │   │   ├── cheating-47-Small-_jpg.rf.273356b180b5410fd091229fedcbbcbd.jpg
│   │   │   │   ├── cheating-47-Small-_jpg.rf.81558cd6bb93764aa27e57d8ab12e761.jpg
│   │   │   │   ├── cheating-49-Small-_jpg.rf.5994a894363c8caef9f28c0a3804d16f.jpg
│   │   │   │   ├── cheating-49-Small-_jpg.rf.d2020157d4f2c97061cdbe5eb65078f3.jpg
│   │   │   │   ├── cheating-50-Small-_jpg.rf.75ebb4a20d820e2ab0d740b78798d9d4.jpg
│   │   │   │   ├── cheating-50-Small-_jpg.rf.812cecaf6eeec41bcd7a9a375b4ca423.jpg
│   │   │   │   ├── cheating-54-Small-_jpg.rf.394d9f468d0705a32aee1a134ab3db17.jpg
│   │   │   │   ├── cheating-54-Small-_jpg.rf.f115b312dc2a0893e6628e32c24ac7de.jpg
│   │   │   │   ├── cheating-56-Small-_jpg.rf.6c185717e1996e75b4d80aaab40f04ed.jpg
│   │   │   │   ├── cheating-56-Small-_jpg.rf.8036e87a8db18020dbb3cb30710a98f1.jpg
│   │   │   │   ├── cheating-57-Small-_jpg.rf.04553ffbc92102a2f35418776774538a.jpg
│   │   │   │   ├── cheating-57-Small-_jpg.rf.c051b9189bc06905955ae81abe1f6621.jpg
│   │   │   │   ├── cheating-58-Small-_jpg.rf.396a347b8e72f3479b3790bda283376b.jpg
│   │   │   │   ├── cheating-58-Small-_jpg.rf.522c0c3e389669a0165bedfefe298b33.jpg
│   │   │   │   ├── cheating-59-Small-_jpg.rf.07477cd8dff1e10fe812f285c06a9ca2.jpg
│   │   │   │   ├── cheating-59-Small-_jpg.rf.d0f8df8f7a564ff1a8e21d4895d0bdac.jpg
│   │   │   │   ├── cheating-60-Small-_jpg.rf.026c3445ccc44fcd48c0ce45800437c1.jpg
│   │   │   │   ├── cheating-60-Small-_jpg.rf.4fc95ed29086c6f722fe7bc070d46e53.jpg
│   │   │   │   ├── cheating-61-Small-_jpg.rf.62e6f547c139f47129fcdbad252b7fe5.jpg
│   │   │   │   ├── cheating-61-Small-_jpg.rf.eecbd4e579365cdbbb797ba9d07eedde.jpg
│   │   │   │   ├── cheating-62-Small-_jpg.rf.6aac126cfc77faa13ebddcc36b44e2d2.jpg
│   │   │   │   ├── cheating-62-Small-_jpg.rf.91928b62e427e857aef2f1b4a7575a15.jpg
│   │   │   │   ├── cheating-7-Small-_jpg.rf.4860c875680755b027ff4efe7abdd660.jpg
│   │   │   │   └── cheating-7-Small-_jpg.rf.b756bef556b9fe2e441ba142bdabf8c6.jpg
│   │   │   └── not cheating/
│   │   │       ├── Not-Cheating-11-_jpg.rf.89a38effe1964165cd5b14c21bd799e6.jpg
│   │   │       ├── Not-Cheating-11-_jpg.rf.9c94561708fa292872e3535c34a80ac6.jpg
│   │   │       ├── Not-Cheating-12-_jpg.rf.971c8429fdd1b8ec33997a24048c33a4.jpg
│   │   │       ├── Not-Cheating-12-_jpg.rf.9c03713c5eefc1fab5ab6731e542e7d3.jpg
│   │   │       ├── Not-Cheating-14-_jpg.rf.9c1c388464e488658b2bcd85cf8efa37.jpg
│   │   │       ├── Not-Cheating-14-_jpg.rf.fd7a5ca69b82efd74994b2b76e2dd317.jpg
│   │   │       ├── Not-Cheating-15-_jpg.rf.39793d70b210059d66043f70dbb29079.jpg
│   │   │       ├── Not-Cheating-15-_jpg.rf.a34ccfcc53566d307df672aa4d59c2b0.jpg
│   │   │       ├── Not-Cheating-16-_jpg.rf.043160b24bc9a08f817f6908095f21d3.jpg
│   │   │       ├── Not-Cheating-16-_jpg.rf.4957860b7f6e6301e1fe0b16c8702aaf.jpg
│   │   │       ├── Not-Cheating-19-_jpg.rf.6924de77127254db658b00c8b1c63b45.jpg
│   │   │       ├── Not-Cheating-19-_jpg.rf.aeeba65fc706056fdac810740cc9c953.jpg
│   │   │       ├── Not-Cheating-20-_jpg.rf.14d50fb552a1f2c7ce6beff99afc881c.jpg
│   │   │       ├── Not-Cheating-20-_jpg.rf.892d681586f7e2a40321c49e4574160e.jpg
│   │   │       ├── Not-Cheating-21-_jpg.rf.3db3c42223fb9e6527be0c164d9f4e4e.jpg
│   │   │       ├── Not-Cheating-21-_jpg.rf.aaf38a9c246017bcba3deeb7b4cf3609.jpg
│   │   │       ├── Not-Cheating-22-_jpg.rf.59cab5206d2b664ddcc6321f0065f31b.jpg
│   │   │       ├── Not-Cheating-22-_jpg.rf.6306242dce953af32ec97fe636723df3.jpg
│   │   │       ├── Not-Cheating-26-_jpg.rf.5e8b95bf046cf67f731d5693502de5ed.jpg
│   │   │       ├── Not-Cheating-26-_jpg.rf.aede5ba0538db7347d0007c4cb008855.jpg
│   │   │       ├── Not-Cheating-27-_jpg.rf.1a23869508a997c7fb82c53ede86de1f.jpg
│   │   │       ├── Not-Cheating-27-_jpg.rf.42d8dce3530a594a2c34d4a4f25ed7e9.jpg
│   │   │       ├── Not-Cheating-28-_jpg.rf.7d812f5a34238bde22a4540c9dd0edb2.jpg
│   │   │       ├── Not-Cheating-28-_jpg.rf.e68da52e2d533fdeaece251ecda33b02.jpg
│   │   │       ├── Not-Cheating-30-_jpg.rf.353449e595bc0e0e9f43f86a9710a418.jpg
│   │   │       ├── Not-Cheating-30-_jpg.rf.f1787cb07fc434315db4179a49237628.jpg
│   │   │       ├── Not-Cheating-31-_jpg.rf.004c58c318a2c1fe5abdec0c39e58b13.jpg
│   │   │       ├── Not-Cheating-31-_jpg.rf.8e6c750e5c2529e5e8f092d7e1194fdb.jpg
│   │   │       ├── Not-Cheating-32-_jpg.rf.55c23e2d1d5433a4ab80afc209055714.jpg
│   │   │       ├── Not-Cheating-32-_jpg.rf.7c6761d89f9d4da288a3801ec930b58d.jpg
│   │   │       ├── Not-Cheating-35-_jpg.rf.046bdd0077153537e2c2c03c9c933f12.jpg
│   │   │       ├── Not-Cheating-35-_jpg.rf.fc363cc832251c4000f228f12ae1a887.jpg
│   │   │       ├── Not-Cheating-36-_jpg.rf.23c300d8dda4fa916114554a13c49840.jpg
│   │   │       ├── Not-Cheating-36-_jpg.rf.dc22f15ce78ad3484dedc4bd7eead188.jpg
│   │   │       ├── Not-Cheating-39-_jpg.rf.6e7f64be49d9bc067f0e1d592f7a2d9b.jpg
│   │   │       ├── Not-Cheating-39-_jpg.rf.be21ade7b151f01e86212ad9a44a669e.jpg
│   │   │       ├── Not-Cheating-4-_jpg.rf.771f543b40201738ae69869bf5862170.jpg
│   │   │       ├── Not-Cheating-4-_jpg.rf.9bb0679a07cff52396a3ac7740915325.jpg
│   │   │       ├── Not-Cheating-40-_jpg.rf.a5db432cf7b35f58b5c216c256ef5b82.jpg
│   │   │       ├── Not-Cheating-40-_jpg.rf.ac35d49fe197e1c003bce6107b2bb7e3.jpg
│   │   │       ├── Not-Cheating-42-_jpg.rf.1faa7c57edf4f5d460aacbb2d303832a.jpg
│   │   │       ├── Not-Cheating-42-_jpg.rf.bbca235510ee946b2671e67c3357eb2b.jpg
│   │   │       ├── Not-Cheating-43-_jpg.rf.449b97311b48900fe3c0d85329f3c7e0.jpg
│   │   │       ├── Not-Cheating-43-_jpg.rf.5266b73986b85b7ebc88bd9999bc44b6.jpg
│   │   │       ├── Not-Cheating-44-_jpg.rf.7f82265e7b3079018c177c9f9ecf2e09.jpg
│   │   │       ├── Not-Cheating-44-_jpg.rf.8a5d9d92fd6216c3f2263e5fb735ac68.jpg
│   │   │       ├── Not-Cheating-46-_jpg.rf.b7b3015475f9b60f215a7feb302bf115.jpg
│   │   │       ├── Not-Cheating-46-_jpg.rf.c1c787a68d523a07d7d98ee1f72ae84c.jpg
│   │   │       ├── Not-Cheating-48-_jpg.rf.29b16d024c4457c2e3cf93e8e10049d4.jpg
│   │   │       ├── Not-Cheating-48-_jpg.rf.83559783d6a94b39a5a8244c0e5a2f98.jpg
│   │   │       ├── Not-Cheating-49-_jpg.rf.19a944d8a4c5a879f827ba3db9b580f8.jpg
│   │   │       ├── Not-Cheating-49-_jpg.rf.ff666842ff88074930ff5814e8b9fc93.jpg
│   │   │       ├── Not-Cheating-5-_jpg.rf.043d9ce4844d666f0ba8b0eb34f1fa1e.jpg
│   │   │       ├── Not-Cheating-5-_jpg.rf.5071f55aaf1d1d00c9bb478ead69a9ff.jpg
│   │   │       ├── Not-Cheating-50-_jpg.rf.093e860843033204b93cdd436eee5240.jpg
│   │   │       ├── Not-Cheating-50-_jpg.rf.6e2214824bd8c8437f82cbd00cf4e8ee.jpg
│   │   │       ├── Not-Cheating-54-_jpg.rf.e002e40a099eb01b7515b99cad0f7b03.jpg
│   │   │       ├── Not-Cheating-54-_jpg.rf.e4f06f219bae9b7985d391b10b925b0f.jpg
│   │   │       ├── Not-Cheating-55-_jpg.rf.c453dc41d6194a434dfadc571dd5d073.jpg
│   │   │       ├── Not-Cheating-55-_jpg.rf.e88bc672d937ac9f08956e72f59f9e31.jpg
│   │   │       ├── Not-Cheating-56-_jpg.rf.f9860057c02bec2636b3d6b169579523.jpg
│   │   │       ├── Not-Cheating-56-_jpg.rf.fa3f137129ae6447a511ec11a8aebaa0.jpg
│   │   │       ├── Not-Cheating-57-_jpg.rf.ae83fddf873eb6bb9b2f241a2a067bbe.jpg
│   │   │       ├── Not-Cheating-57-_jpg.rf.f6281de068ea025e7834d1786ddc2faf.jpg
│   │   │       ├── Not-Cheating-58-_jpg.rf.c7d413495fc38c68f41a0a8b74e49a2d.jpg
│   │   │       ├── Not-Cheating-58-_jpg.rf.cf23bb35c1fa4b3e7e06df77eb740c05.jpg
│   │   │       ├── Not-Cheating-59-_jpg.rf.389269cac4d5632639f4757bd6f28fff.jpg
│   │   │       ├── Not-Cheating-59-_jpg.rf.ed4ea0f63fd09927a4ecce1dca840dd5.jpg
│   │   │       ├── Not-Cheating-6-_jpg.rf.19d7bbabe0cded1d05dd0b9a8822e635.jpg
│   │   │       ├── Not-Cheating-6-_jpg.rf.3a5680619ff71e65bbfcc1fcf746f0aa.jpg
│   │   │       ├── Not-Cheating-61-_jpg.rf.94f8d5b52a99a1edf7abf37503ec6c40.jpg
│   │   │       ├── Not-Cheating-61-_jpg.rf.9db461ab3695d78208e10760535e71f2.jpg
│   │   │       ├── Not-Cheating-62-_jpg.rf.02c320d9b4f6e5723de92adc39320a64.jpg
│   │   │       ├── Not-Cheating-62-_jpg.rf.3e427c8deb2bd4b6443949449e74de0b.jpg
│   │   │       ├── Not-Cheating-63-_jpg.rf.95523b99f6bd6beda9540157bc12a38a.jpg
│   │   │       ├── Not-Cheating-63-_jpg.rf.b8120474429f279361d795e3c711f2b4.jpg
│   │   │       ├── Not-Cheating-8-_jpg.rf.9fec0790c2d97898f0775a0b33291cd3.jpg
│   │   │       ├── Not-Cheating-8-_jpg.rf.cd2e54c42b0ab93d7902f41e5a0b0275.jpg
│   │   │       ├── Not-Cheating-9-_jpg.rf.931e62a919e9a7ecd9accdf274d3b435.jpg
│   │   │       └── Not-Cheating-9-_jpg.rf.bef83fbd7b0f3a9c3e6225d6455c7276.jpg
│   │   └── valid/
│   │       ├── _tokenization.txt
│   │       ├── cheating/
│   │       │   ├── cheating-10-_jpg.rf.ff543b918c05f65c9dbae699929da7df.jpg
│   │       │   ├── cheating-16-Small-_jpg.rf.4af3d1b366b886a6dbce6a0422034f3a.jpg
│   │       │   ├── cheating-2-Small-_jpg.rf.fb7d34f8481cd79b857bc1553e4a9658.jpg
│   │       │   ├── cheating-27-Small-_jpg.rf.6dbc62b8bfe77eab0357268e19baceb3.jpg
│   │       │   ├── cheating-31-Small-_jpg.rf.8a71c43ca998fb4eae2ca5e3313da2ac.jpg
│   │       │   ├── cheating-35-Small-_jpg.rf.b4c998c10c1a8c28599a17ce7dfd5dfe.jpg
│   │       │   ├── cheating-48-Small-_jpg.rf.ddf38a1bb2508b98349594616fa02440.jpg
│   │       │   ├── cheating-6-Small-_jpg.rf.0b7868e5c251ffa9a42dcdffa0c5b357.jpg
│   │       │   ├── cheating-8-_jpg.rf.7006155ab1f53d4fed933491a1526841.jpg
│   │       │   └── cheating-9-_jpg.rf.b62d4042d9d27279090f6067c68980b1.jpg
│   │       └── not cheating/
│   │           ├── Not-Cheating-1-_jpg.rf.08b5d570a684a24b822d619855a8b9d1.jpg
│   │           ├── Not-Cheating-10-_jpg.rf.b732d4631014d9311a5f2a9d8578276e.jpg
│   │           ├── Not-Cheating-18-_jpg.rf.6beabf8cb46138ef6bf8c8061d38a8ac.jpg
│   │           ├── Not-Cheating-23-_jpg.rf.62f90aa29064bdab6849e3be45888951.jpg
│   │           ├── Not-Cheating-33-_jpg.rf.03350f3e062200db56673318452c893d.jpg
│   │           ├── Not-Cheating-34-_jpg.rf.f55b5ce75fb8a6ad0daf8aa46e37b056.jpg
│   │           ├── Not-Cheating-37-_jpg.rf.2f8ecec4c715f79c5ab0becc0e7f54c0.jpg
│   │           ├── Not-Cheating-38-_jpg.rf.f2f455895f009fe7dbe761e859e3eb06.jpg
│   │           ├── Not-Cheating-45-_jpg.rf.5122b87bcfa89893d4859906d4a7b4b2.jpg
│   │           ├── Not-Cheating-51-_jpg.rf.2e97e7b92ec598d6372ff72c525cc954.jpg
│   │           ├── Not-Cheating-53-_jpg.rf.e9bf1a635eddd27c5f8de33ac4e15480.jpg
│   │           ├── Not-Cheating-60-_jpg.rf.a70025ee7962a2c17f3af1eb699dca94.jpg
│   │           └── Not-Cheating-7-_jpg.rf.559cc53817643cb2f08ee87d70f1d459.jpg
│   ├── Offline-capabilities/
│   │   ├── ML-Model-Optimisation.py
│   │   ├── local-storage.py
│   │   ├── processing-data.py
│   │   ├── readme.md
│   │   ├── resource-management.py
│   │   └── video-processing.py
│   ├── SQLFILE.sql
│   ├── __pycache__/
│   │   ├── audio.cpython-311.pyc
│   │   ├── audio.cpython-312.pyc
│   │   ├── detection.cpython-311.pyc
│   │   ├── head_pose.cpython-311.pyc
│   │   └── head_pose.cpython-312.pyc
│   ├── audio.py
│   ├── detection.py
│   ├── face-rec.py
│   ├── graph.py
│   ├── head_pose.py
│   ├── logic.xlsx
│   ├── model_training.py
│   ├── mtcnn_face_detection.py
│   ├── object_detection.py
│   ├── peer_comparison_tool.py
│   ├── processes.py
│   ├── proctor_api.py
│   ├── proctor_core.py
│   ├── pyaudio_test.py
│   ├── run.py
│   ├── screen_recorder.py
│   ├── test-image.jpg
│   ├── test-image2.jpg
│   └── train.py
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── GSSoC-Ext.png
├── GUI/
│   ├── active.html
│   ├── copypaste.html
│   └── windowClose.html
├── LICENSE
├── PROJECT_STRUCTURE.md
├── ReadMe.md
├── SECURITY.md
├── SECURITYPOLICY.md
├── Suggested-Issues.md
├── Userdb.sql
├── __pycache__/
│   ├── audio.cpython-311.pyc
│   ├── detection.cpython-311.pyc
│   ├── head_pose.cpython-311.pyc
│   └── tutorial/
│       └── tutorial.html
├── calenderApp/
│   └── calender.html
├── contributor/
│   ├── contributor.css
│   ├── contributor.html
│   └── contributor.js
├── frontend/
│   └── index.html
├── heatmap_combined_20241009_144503.png
├── login.py
├── modle.png
├── repo_structure.txt
├── requirements.txt
└── templates/
    └── login.html
```
<!-- END_STRUCTURE -->