# Make_high-resolution_IMG
Vision Agent - Make high-resolution IMG
---
딥러닝을 이용하여 저해상도 이미지를 고해상도로 만들어서 출력 및 저장하는 프로그램입니다.
고전방식과의 비교를 위해 Bicubic 방법의 출력도 지원합니다.

Super-Resolution을 위해 opencv-contrib-python 설치가 필요합니다.
```python
pip install opencv-contrib-python
```

![image](https://github.com/star77sa/Make_high-resolution_IMG/assets/73769046/d2b646e9-014e-432f-ad40-9fc5328fb326)



1. examples 폴더에 변환을 원하는 이미지를 넣은 뒤 '이미지 열기' 버튼으로 파일을 열어줍니다.
2. Scale (x2, x4, x8) 선택 및 Bicubic / Super-Resolution 방법 선택을 한 뒤에 '이미지 변환' 버튼으로 변환된 이미지를 출력합니다.
3. '내보내기'버튼을 통하여 이미지를 result 폴더의 result.png 로 저장합니다. (이미지 저장은 super-resolution 방식으로만 저장이 됩니다.)
4. '나가기'버튼을 통하여 프로그램을 종료합니다.
---
5. Real Time 버튼은 웹캠을 통하여 실시간으로 Bicubic 방법과 Super-Resolution 방법을 적용한 출력물을 보여줍니다. 'q' 버튼을 통하여 프로그램을 종료할 수 있습니다.
