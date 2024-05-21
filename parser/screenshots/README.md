# Парсеры

## Yandex

### Виды цен

**Уточнение:** Скидка по карте Пэй может у разных пользователей отличаться (?)

1. Тип 1 ([Ссылка](https://market.yandex.ru/product--blesk-dlia-gub-le-grand-volume/664040634?sku=100928907750&uniqueId=924574&do-waremd5=TkWAAtMswRA95y8XyphX9g))

![](yandex_type1.png)

- Цена 1: ``<span data-auto="price-value">468</span>``
- Скидка: ``<div data-auto="discount-badge" class="_1ixhg _1eCg2">–10&thinsp;%</div>``
- Цена 2: Посчитать через cкидку или получить весь блок через ``<div data-auto="offer-price" ...> `` и найти последний span c пустым классом ``<span class=""><span class="_1DwfQ">521&nbsp;₽</span></span>``

Самый Родительский div: ``<div class="idECc" data-walter-collection="price">``
Следующий родительский ``<div class="" data-zone-name="price" data-node-id="ckn7_3015_2" data-baobab-name="price">``
2. Тип 2 ([Ссылка](https://market.yandex.ru/product--influence-beauty-blesk-dlia-gub-plexiglass-lip-gloss-ton-shade-05/1663269245?sku=101598313596&do-waremd5=qQQj7zd0a0xAo-_lhsciQg&showUid=17159736558560672185106002&uniqueId=993469&cpa=1&cpc=PRz2zu4wZJnHLMAhDovzql3cRPbyPHyY47KUTB4BgfB8URJ-_CH74BJ48gd5JEyTHPYvjq8i0qEIKwCNWb76EyNeAroVAiS_RWZodD5Yw8JjB8suN5lnhk9p-PlCN9u0Uyh24NwH_gH8DN-Z0ECogEN9Kl1ZDt5fhQD7KFWTrN10mQ-CNk1W5_jDJfoYSrmYuipRdw6xAkoxlEIxXjrBHqI9vCbFEZbpKYsEr6caVCLup-RPAhyRbV8h88kiX2JtTrknMilLOFB9G2v_lnV9WzXyyR4b_n8AAovsS6eBw7Y%2C&sponsored=1))

![](yandex_type2.png)

- Цена 1: ``<h3 class="Jdxhz" data-auto="snippet-price-current"><span class="_3gYEe">Цена с картой Яндекс Пэй:</span>538<!-- --> <span class="_2MxwE">₽</span></h3>``
- Скидка: ``<div class="cia-vs" data-zone-name="discount-badge"><span class="_3gYEe">Скидка: 1%</span><div data-auto="discount-badge" class="_1ixhg _3PeLm">–1&thinsp;%</div></div>``
- Цена 2: ``<span class="_2r9lI" data-auto="snippet-price-old"><span aria-hidden="true">без:<!-- -->&nbsp;</span><span class="_3gYEe">Вместо: </span>543<!-- -->&thinsp;<span class="_39uKu">₽</span></span>``

3. Тип 3 ([Ссылка](https://market.yandex.ru/product--tint-dlia-gub-lip-tint-aqua-gel/1764396919?sku=101799569511&uniqueId=892157&do-waremd5=cw_YDFIVe8cPGR_7QS57rw))

![](yandex_type3.png)

- Цена 1: ``<h3 class="Jdxhz" data-auto="snippet-price-current"><span class="_3gYEe">Цена с картой Яндекс Пэй:</span>302<!-- --> <span class="_2MxwE">₽</span></h3>``
- Скидка: ``<div data-auto="discount-badge" class="_1ixhg _3PeLm">–6&thinsp;%</div>``
- Цена 2: ``<span class="_2r9lI" data-auto="snippet-price-old"><span aria-hidden="true">без:<!-- -->&nbsp;</span><span class="_3gYEe">Вместо: </span>305<!-- -->&thinsp;<span class="_39uKu">₽</span><s class="_347Sb">322</s>&thinsp;<span class="_39uKu">₽</span></span>``
- Цена 3: ``<span class="_2r9lI" data-auto="snippet-price-old"><span aria-hidden="true">без:<!-- -->&nbsp;</span><span class="_3gYEe">Вместо: </span>305<!-- -->&thinsp;<span class="_39uKu">₽</span><s class="_347Sb">322</s>&thinsp;<span class="_39uKu">₽</span></span>``

## WB

1. Тип 1 ([Ссылка](https://www.wildberries.ru/catalog/64775386/detail.aspx))

![](wb_type1.png)

- Цена 1: ``//ins[@class="price-block__final-price"]``
- Цена 2: ``//del[@class="price-block__old-price"]``

2. Тип 2 ([Ссылка]())

![](wb_type2.png)

- Цена 1: ``//span[@class="price-block__wallet-price"]``
- Цена 2: ``//ins[@class="price-block__final-price wallet"]``
- Цена 3: ``//del[@class="price-block__old-price"]``
