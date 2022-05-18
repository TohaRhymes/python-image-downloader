# Отчет

(Все выводы написаны после каждого из двух блоков)

# Launching

```
usage: downloader.py [-h] [-in FILE] [-out OUT_DIR] [-wrks WORKERS] [-vb VERBOSE] [-pp POSTPROCESSING]

options:
  -h, --help            show this help message and exit
  -in FILE, --file FILE
                        File with links to image.
  -out OUT_DIR, --out_dir OUT_DIR
                        Output directory.
  -wrks WORKERS, --workers WORKERS
                        Amount of python workers (python threads work in parallel).
  -vb VERBOSE, --verbose VERBOSE
                        Verbosity of the output.
  -pp POSTPROCESSING, --postprocessing POSTPROCESSING
                        Make post-processing?.
```

## 1. Without post-processing

* 1 worker

```
$ python downloader.py -in data/images2000.txt -out kek1 -wrks 1

2001it [06:52,  4.85it/s]
Download finished (errors: 1, successes: 2000).
Total time: 412.8402898311615
Program finished, total time: 412.8404185771942
```

* 2 workers

```
$ python downloader.py -in data/images2000.txt -out kek2 -wrks 2

2001it [02:50, 11.74it/s]
Download finished (errors: 1, successes: 2000).
Total time: 170.49827194213867
Program finished, total time: 170.49843406677246
```

* 5 workers

```
$ python downloader.py -in data/images2000.txt -out kek5 -wrks 5

2001it [02:03, 16.26it/s]
Download finished (errors: 1, successes: 2000).
Total time: 123.13065838813782
Program finished, total time: 123.13081526756287
```

* 10 worker

```
$ python downloader.py -in data/images2000.txt -out kek10 -wrks 10

2001it [01:11, 28.00it/s]
Download finished (errors: 1, successes: 2000).
Total time: 71.57289791107178
Program finished, total time: 71.5730881690979
```

* 50 workers

```
$ python downloader.py -in data/images2000.txt -out kek50 -wrks 50

2001it [00:43, 46.29it/s] 
Download finished (errors: 1, successes: 2000).
Total time: 43.93788743019104
Program finished, total time: 43.93803405761719
```

* 100 workers

```
$ python downloader.py -in data/images2000.txt -out kek100 -wrks 100

2001it [00:39, 50.44it/s] 
Download finished (errors: 1, successes: 2000).
Total time: 41.08422303199768
Program finished, total time: 41.084357500076294
```

* 1000 workers

```
$ python downloader.py -in data/images2000.txt -out kek1000 -wrks 1000

2001it [00:08, 238.20it/s]
Download finished (errors: 304, successes: 1697).
Total time: 24.602120876312256
Program finished, total time: 24.60224986076355
```

### Вывод

Время работы для 1, 2, 5, 10, 50, 100 и 1000 воркеров: 413, 170, 123, 72, 44, 41, 24 секунд соответственно. 
Видно, что сначала при увеличении количества воркеров время уменьшается даже больше чем в два раза, но потом уже не так быстро.
Возможно это связано с затратностью на переключение между тредами (так как это тоже занимает ресурсы и время), а так же скорости интернета.



## 2. With post-processing

* 1 worker

```
$ python downloader.py -in data/images2000.txt -out kek1 -wrks 1 -pp

2001it [04:42,  7.09it/s]
Download finished (errors: 1, successes: 2000).
Total time of downloading: 282.10252475738525
2000it [01:17, 25.89it/s]
Post processing finished, total time: 77.2725579738617
Program finished, total time: 359.3768002986908
```

* 2 workers

```
$ python downloader.py -in data/images2000.txt -out kek2 -wrks 2 -pp

2001it [02:39, 12.58it/s]
Download finished (errors: 1, successes: 2000).
Total time of downloading: 159.13726353645325
2000it [01:21, 24.53it/s]
Post processing finished, total time: 81.56836771965027
Program finished, total time: 240.70727729797363
```

* 5 workers

```
$ python downloader.py -in data/images2000.txt -out kek5 -wrks 5 -pp

2001it [01:18, 25.54it/s]
Download finished (errors: 1, successes: 2000).
Total time of downloading: 78.40597414970398
2000it [01:54, 17.54it/s]
Post processing finished, total time: 114.13465547561646
Program finished, total time: 192.54260897636414
```

* 10 worker

```
$ python downloader.py -in data/images2000.txt -out kek10 -wrks 10 -pp

2001it [01:13, 27.24it/s]
Download finished (errors: 1, successes: 2000).
Total time of downloading: 73.5360951423645
2000it [02:04, 16.05it/s]
Post processing finished, total time: 125.01079154014587
Program finished, total time: 198.5486192703247
```

* 50 workers

```
$ python downloader.py -in data/images2000.txt -out kek50 -wrks 50 -pp

2001it [00:52, 38.16it/s]
Download finished (errors: 1, successes: 2000).
Total time of downloading: 53.0095100402832
2000it [02:02, 16.33it/s]
Post processing finished, total time: 127.9489586353302
Program finished, total time: 180.96065044403076
```

* 100 workers

```
$ python downloader.py -in data/images2000.txt -out kek100 -wrks 100 -pp

2001it [01:24, 23.74it/s] 
Download finished (errors: 2, successes: 1999).
Total time of downloading: 85.64498090744019
2000it [02:00, 16.64it/s]
Post processing finished, total time: 136.76569366455078
Program finished, total time: 222.41244983673096
```

* 1000 workers

```
$ python downloader.py -in data/images2000.txt -out kek1000 -wrks 1000 -pp

2001it [00:07, 255.65it/s]
Download finished (errors: 332, successes: 1669).
Total time of downloading: 23.43959379196167
1669it [00:11, 151.42it/s] 
Post processing finished, total time: 101.1770749092102
Program finished, total time: 124.61890602111816
```

### Вывод

Интересно, что тут поменялось даже время скачивания. Так как постпроцессинг происходит после скачивания, скорее всего, это связано с нестабильностью интернета, а следовательно в идеальном эксперименте необходимо было бы повторить несколько раз 1 и тот же эксперимент (желательно на разных ЭВМ с разным подключением), чтобы судить о настоящем изменением скорости.

Второе, время пост-обработки: для 1, 2, 5, 10, 50, 100 и 1000 воркеров она составила соответственно: 77 ,82, 114(0_о), 125, 127, 136, 101. 
Это СУПЕР странный результат, так как время УВЕЛИЧИВАЕТСЯ при увеличении количества воркеров, а должно уменьшаться (Хотя запуск идет точно так же, как и запуск скачивания файлов). Тут, видимо, действительно очень сильно играет переключение процессов, так как мы не просто ждем ответа от сервера, а читаем много файлов, и затем переключаемся (можем переключиться) на середине, соответственно шины I/O постоянно заняты. 

Разумные комментарии дать сложно, наверное, надо копать в стороны архитектуры. 

