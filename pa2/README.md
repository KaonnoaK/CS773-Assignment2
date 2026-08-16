<p align="center">
  <h1 align="center"> Programming Assignment 2 - “Dilwale Dulhania “NAHI” Le Jayenge” </h1>

  <h2> Team Members : </h2>
  <h4> Bhavani Onkar - 24M1094 </h4>
  <h4> Mohith Sai Babu Kota - 23M1169 </h4>
  <h4> Satvikkumar Patel - 23M1117 </h4>

<p>

  Task 1:
  - way partitioning : 
   the LLC has 16 ways, the first 8 ways will be assigned to cpu core 0 and the next eight to the core 1.
  
  Task 2A:
  - static set paritioning :
   The LLC has 4096 sets, the addresses from core 0 goes former 2048 sets , and core 1 to the later. 
   The most significant bit in the set index is used to compare against the cpu core. 

  Task 2B:
  - dynamic set partitioning :
    It starts with having half the sets assigned to each core. After every core makes some 'x' number of accesses , its miss is evaluated, if its more than threshold, the allotted sets are proportionally increased. 

</p>

# Repository Setup

```bash
git clone [your-repository-link]
