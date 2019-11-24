Расход памяти - 1.5 Гб (свап - 1гб)

Время запуска контейнера - 23 минуты
Размер файла - 12Mb (без лиц)  6000x3376
Время обработки
181094
227613
219200
224901
217642
239144

Чтение с сд карты 
1800
2340
2260
2005
2292
2029

Распознание фото с лицом - 12Mb   6000x3376
Время работы контейнера - 23 минуты

на pi3
179222
231847
215715
235820
236794
272249

чтение с карты
1803
1923
2343
2127
2392
2028

Вывод: по мере нагревания малины, время обработки будет увеличиваться (на 50% вполне возможный сценарий)



Распознание на компе i7 
/home/ssr/Programming/Python/photo-recognition/venv/bin/python /home/ssr/Programming/Python/photo-recognition/photo_recognition/producer_test.py
kafka host: 192.168.100.201:32769
{'kafka-metrics-count': {'count': 50.0}, 'consumer-metrics': {'connection-close-rate': 0.0, 'connection-creation-rate': 0.03321405923557178, 'select-rate': 0.0, 'io-wait-time-ns-avg': 0.0, 'io-wait-ratio': 0.0, 'io-time-ns-avg': 0.0, 'io-ratio': 0.0, 'connection-count': 1.0, 'network-io-rate': 0.132855971922564, 'outgoing-byte-rate': 2.2585497095659206, 'request-rate': 0.06642788146200794, 'request-size-avg': 34.0, 'request-size-max': 36.0, 'incoming-byte-rate': 61.82011908164226, 'response-rate': 0.06665237285701882, 'request-latency-avg': 53.418636322021484, 'request-latency-max': 102.30565071105957}, 'consumer-node-metrics.node-bootstrap-0': {'outgoing-byte-rate': 2.2585393437167696, 'request-rate': 0.06642758466431632, 'request-size-avg': 34.0, 'request-size-max': 36.0, 'incoming-byte-rate': 61.81986306287835, 'response-rate': 0.06665209845328567, 'request-latency-avg': 53.418636322021484, 'request-latency-max': 102.30565071105957}, 'consumer-fetch-manager-metrics': {'fetch-size-avg': 0.0, 'fetch-size-max': -inf, 'bytes-consumed-rate': 0.0, 'records-per-request-avg': 0.0, 'records-consumed-rate': 0.0, 'fetch-latency-avg': 0.0, 'fetch-latency-max': -inf, 'fetch-rate': 0.0, 'records-lag-max': -inf, 'fetch-throttle-time-avg': 0.0, 'fetch-throttle-time-max': -inf}, 'consumer-coordinator-metrics': {'heartbeat-response-time-max': -inf, 'heartbeat-rate': 0.0, 'join-time-avg': 0.0, 'join-time-max': -inf, 'join-rate': 0.0, 'sync-time-avg': 0.0, 'sync-time-max': -inf, 'sync-rate': 0.0, 'last-heartbeat-seconds-ago': inf, 'commit-latency-avg': 0.0, 'commit-latency-max': -inf, 'commit-rate': 0.0, 'assigned-partitions': 0.0}}
ConsumerRecord(topic='image_process', partition=0, offset=0, timestamp=1573755855977, timestamp_type=0, key=None, value={'path': '/home/ssr/Pictures/Калуга трип/калуга камера/DSC01995.JPG', 'file': 'DSC01995.JPG'}, headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=203, serialized_header_size=-1)
/home/ssr/Pictures/Калуга трип/калуга камера/DSC01995.JPG
time for read: 479, time for location: 10061
[]
ConsumerRecord(topic='image_process', partition=0, offset=1, timestamp=1573755855978, timestamp_type=0, key=None, value={'path': '/home/ssr/Pictures/Калуга трип/калуга камера/DSC01915.JPG', 'file': 'DSC01915.JPG'}, headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=203, serialized_header_size=-1)
/home/ssr/Pictures/Калуга трип/калуга камера/DSC01915.JPG
time for read: 320, time for location: 10019
[(2908, 2883, 2983, 2808)]
ConsumerRecord(topic='image_process', partition=0, offset=2, timestamp=1573755855979, timestamp_type=0, key=None, value={'path': '/home/ssr/Pictures/Калуга трип/калуга камера/DSC01837.JPG', 'file': 'DSC01837.JPG'}, headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=203, serialized_header_size=-1)
/home/ssr/Pictures/Калуга трип/калуга камера/DSC01837.JPG
time for read: 358, time for location: 9883
[]
ConsumerRecord(topic='image_process', partition=0, offset=3, timestamp=1573755855980, timestamp_type=0, key=None, value={'path': '/home/ssr/Pictures/Калуга трип/калуга камера/DSC01912.JPG', 'file': 'DSC01912.JPG'}, headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=203, serialized_header_size=-1)
/home/ssr/Pictures/Калуга трип/калуга камера/DSC01912.JPG
time for read: 300, time for location: 9785
[]
ConsumerRecord(topic='image_process', partition=0, offset=4, timestamp=1573755855981, timestamp_type=0, key=None, value={'path': '/home/ssr/Pictures/Калуга трип/калуга камера/DSC01908.JPG', 'file': 'DSC01908.JPG'}, headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=203, serialized_header_size=-1)
/home/ssr/Pictures/Калуга трип/калуга камера/DSC01908.JPG
time for read: 356, time for location: 9832
[(142, 3559, 409, 3291)]
ConsumerRecord(topic='image_process', partition=0, offset=5, timestamp=1573755855981, timestamp_type=0, key=None, value={'path': '/home/ssr/Pictures/Калуга трип/калуга камера/DSC01874.JPG', 'file': 'DSC01874.JPG'}, headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=203, serialized_header_size=-1)
/home/ssr/Pictures/Калуга трип/калуга камера/DSC01874.JPG
time for read: 329, time for location: 9844
[(1442, 1769, 1478, 1733), (1762, 1013, 1798, 977)]

Process finished with exit code 0

