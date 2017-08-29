# SeChain
Blockchain System for Education

## 실행방법

1. 가상환경 설정
<pre><code>virtualenv -p python3 venv</code></pre>

2. 가상환경 실행
<pre><code>source ./venv/bin/activate</code></pre>

3. 외부 라이브러리 설치
<pre><code>pip3 install -r requirments.txt
pip3 install --editable .
</code></pre>

4. 실행

> 블록체인 실행
<pre><code>mychain run -p '포트 번호'</code></pre>

> 트랜잭션 전송
<pre><code>mychain sendtx -a 아이피 주소 -m 메세지</code></pre>

