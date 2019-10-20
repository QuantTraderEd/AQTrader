
## Test tick count recording under different virtual computing power
### 1.test1
CPU: Intel(R) Xeon(R) E-2136 CPU @3.31GHz  
RAM: 2.00GB  
OS: Windows Server 2008 64bit  
### 2.test2
CPU: Intel(R) Xeon(R) E3-1230 V6 @3.50GHz  
RAM: 4.00GB  
OS: Windows Server 2016 64bit  


```python
import bs4
import pandas as pd
```


```python
date_lst = ['20191011','20191014', '20191015', '20191016', '20191018']
df_test1_count = pd.DataFrame()
df_test2_count = pd.DataFrame()
```


```python
def find_count(html_text):
    soup = bs4.BeautifulSoup(html_text)
    for line in soup.find_all('pre'):
        line_text = line.get_text()
        if 'shortcd_x' in line_text:
            line_lst = line_text.split('\n')
            text_lst = line_lst[0].split(' ')
            count_lst = [int(item) for item in text_lst]
            print count_lst
    return count_lst
```


```python
def make_df_tmp(str_date, count_lst):
    data_lst = [str_date] + count_lst
    df_tmp = pd.DataFrame(data_lst).transpose()
    df_tmp.columns = ['date', 'big_count', 'mini_count']
    return df_tmp
```


```python
for str_date in date_lst:
    html_text_file = "miniarb_research_%s.html" % str_date
    path = './test1/miniarb_research/'

    f = open(path + html_text_file, 'r')
    html_text = f.read()
    f.close()
    
    count_lst = find_count(html_text)
    df_tmp = make_df_tmp(str_date, count_lst)
    if len(df_test1_count) == 0:
        df_test1_count = df_tmp.copy()
    else:
        df_test1_count = df_test1_count.append(df_tmp)
```

    C:\Anaconda2\lib\site-packages\bs4\__init__.py:166: UserWarning: No parser was explicitly specified, so I'm using the best available HTML parser for this system ("lxml"). This usually isn't a problem, but if you run this code on another system, or in a different virtual environment, it may use a different parser and behave differently.
    
    To get rid of this warning, change this:
    
     BeautifulSoup([your markup])
    
    to this:
    
     BeautifulSoup([your markup], "lxml")
    
      markup_type=markup_type))
    

    [58137, 44322]
    [32903, 27008]
    [53261, 40361]
    [36950, 26616]
    [65450, 51065]
    


```python
for str_date in date_lst:
    html_text_file = "miniarb_research_%s.html" % str_date
    path = './test2/miniarb_research/'

    f = open(path + html_text_file, 'r')
    html_text = f.read()
    f.close()
    
    count_lst = find_count(html_text)
    df_tmp = make_df_tmp(str_date, count_lst)
    if len(df_test2_count) == 0:
        df_test2_count = df_tmp.copy()
    else:
        df_test2_count = df_test2_count.append(df_tmp)
```

    [68327, 52653]
    [65429, 51307]
    [60846, 45695]
    [73436, 52450]
    [74093, 57553]
    


```python
df_test1_count
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>big_count</th>
      <th>mini_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20191011</td>
      <td>58137</td>
      <td>44322</td>
    </tr>
    <tr>
      <th>0</th>
      <td>20191014</td>
      <td>32903</td>
      <td>27008</td>
    </tr>
    <tr>
      <th>0</th>
      <td>20191015</td>
      <td>53261</td>
      <td>40361</td>
    </tr>
    <tr>
      <th>0</th>
      <td>20191016</td>
      <td>36950</td>
      <td>26616</td>
    </tr>
    <tr>
      <th>0</th>
      <td>20191018</td>
      <td>65450</td>
      <td>51065</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_test2_count
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>big_count</th>
      <th>mini_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20191011</td>
      <td>68327</td>
      <td>52653</td>
    </tr>
    <tr>
      <th>0</th>
      <td>20191014</td>
      <td>65429</td>
      <td>51307</td>
    </tr>
    <tr>
      <th>0</th>
      <td>20191015</td>
      <td>60846</td>
      <td>45695</td>
    </tr>
    <tr>
      <th>0</th>
      <td>20191016</td>
      <td>73436</td>
      <td>52450</td>
    </tr>
    <tr>
      <th>0</th>
      <td>20191018</td>
      <td>74093</td>
      <td>57553</td>
    </tr>
  </tbody>
</table>
</div>


