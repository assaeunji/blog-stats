# blog-stats

[GitHub blog](http://assaeunji.github.io/)에 올린 글들의 통계를 파악하기 위한 코드입니다.

`python`의 `requests`와 `bs4` 라이브러리 `BeautifulSoup`모듈을 통해서 제 블로그를 (굳이) 크롤링해봤습니다.

모두 월 별 **누적** 통계를 계산하였고, 
(누적이 아니라 월 별로 통계를 내면 더 좋겠군요 - 코드를 수정해야겠습니다..!)

* 카테고리
* 포스트 제목 
* 포스트 별 단어 수
* 포스트 등록일

를 포함하는 `DataFrame`을 생성하고

* 카테고리 별 포스트 수
* 포스트 별 단어수

에 대한 bar graph를 그릴 수 있도록 했습니다.
