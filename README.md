# Website-CMS-Detection

This Python script is used to detected the website's CMS and Status code. It mainly focus on Opencart, Prestashop, Wordpress, Magento, Shopify and Squarespace. It sends requests to website "https://whatcms.org/" and extracts the detection result from the website. To speed up the detection, a multiple processors method is used.

The input is a .txt file, and each line has a website domanin name, like: "https://www.shore-lines.co.uk/".

The output are three .csv file, "result.csv", "wrong.csv" and "noDetect.csv". "wrong.csv" records the websites that status codes are not 200 or those trigger some issues when runing the code. "noDetection.csv" records the websites that their CMS are not anyone of Opencart, Prestashop, Wordpress, Magento, Shopify and Squarespace. "result.csv"  records all the websites we need.

## Prerequisites
Python3, Chrome browser, chromedriver

## How to use
```
mpiexec -n 20 python3 Main.py -f kent.txt
```
-n is the number of processors you want to use<br>
-f is the file you want to process.<br>

For linux user, if you want to shut down your computer after finishing all the dection, you can use the code in line 52 and 53 in Main.py script. And adding --allow-run-as-root in the command. like:
```
mpiexec --allow-run-as-root -n 20 python3 Main.py -f kent.txt
```
## Authors

* **Hongyi Lin** - *Initial work* - [Hongyi Lin](https://github.com/Hongyil1)

## License

This project is licensed under the MIT License

