# Data Engineer Challenge

The goal of the challenge is to have a tool that is able
to stream data from [kafka](http://kafka.apache.org/) and count unique things within this data.
The simplest use case is that we want to calculate unique users per minute, day, week, month, year. For a very first version, business wants us to provide just the unique users per minute.   

- The data consists of (Log)-Frames of JSON data that are streamed into/from apache kafka.
- Each frame has a timestamp property which is unixtime, the name of the property is `ts`.
- Each frame has a user id property calles `uid`.
- You can assume that 99.9% of the frames arrive with a maximum latency of 5 seconds.
- you want to display the results as soon as possible
- the results should be forwarded to a new kafka topic (again as json.) choose a suitable structure.
- for an advanced solution you should assume that you can *not* guarantee that events are always strictly ordered.

## Requirements:
- provide a Readme that shows how to build and run the code on Linux or OS X
- write a report: what did you do? what was the reasons you did it like that?
- measure at least one performance metric (e.g. frames per second)
- document your approach on how you decide **when** to output the data
- document the estimated error in counting
- it should be possible to ingest historical data. e.g. from the last 2 years.

## sample data

./data-generator -c 1000000 -o stream.jsonl -r 1000 -n 100000

you can just input this file to your kafka topic once by something like

cat stream.jsonl | kafka-console-producer --broker-list localhost:9092 --topic mytopic


## Suggested steps:

#### Basic solution
1. Install kafka (use Docker please)
2. Create a topic
3. Use the kafka producer from kafka itself to send our test data to your topic
4. Create a small app that reads this data from kafka and prints it to stdout
5. Find a suitable data structure for counting and implement a simple counting mechanism, output the results to stdout
##### Advanced solution
6. benchmark
7. Output to a new Kafka Topic instead of stdout
8. try to measure performance and optimize
9. write about how you could scale
10. only now think about the edge cases, options and other things

## Evaluation Criteria & Expectations

- ability to break down *business* requirements into simple prototype code
- clean project setup and documentation
- research and use of suitable data structure for a specific use case. explain which and why.
- ability to write performant code to handle streaming data. measure and document _how_ fast your solution is.
- Understanding how to benchmark and analyze performance bottle necks. what tools did you use?
- awareness of the mechanisms and costs of serialization. Explain (and ideally prove!) why json is an ideal format here or why not and then suggest a better solution.
- scalability: _explain_ how you _would_ scale your approach


## Bonus Questions / Challenges:

- how do you scale it to improve troughput.
- you may want count things for different time frames but only do json parsing once.
- explain how you would cope with failure if the app crashes mid day / mid year.
- when creating e.g. per minute statistics, how do you handle frames that arrive late or frames with a random timestamp, describe a strategy?
- make it accept data also from std-in (instead of kafka) for rapid prototyping. (this might be helpful to have for testing anyways)
- measure also the performance impact / overhead of the json parser

## Hints:

- tap into other peoples know-how and code.
- you should not use any big data framework, just your favourite fast programming language that has a Kafka driver. 
- If you found the cheatcode for level 5 (well done!) you should try to archieve level 10 ;)
- check that your last commit compiles.
- be smart and impress us. It does not matter if you impress us with nice clean code or with a very clever hack to archieve the business goal in short time.