
# def graph():
#     # 차트 레이아웃을 설정
#     fig = plt.figure(figsize=(10,10)) #최초의 창 크기를 10x10으로 설정, 크기를 설정하지 않으면 아무 것도 나오지 않음

#     #ax_main 실제로 데이터가 그려지는 영역
#     ax_main = fig.add_subplot(1,1,1) #1,1,1의 의미는 전체 창을 1x1로 쪼개고 ax_main을 생성한다는 뜻

#     # x축에 쓰일 날짜 값 조정
#     def x_date(x,pos):
#         try:
#             return index[int(x-0.5)][:7] # 0:6까지만 잘라서 2019-01와 같이 표현
#         except IndexError:
#             return ''

#     # x축을 조정
#     ax_main.xaxis.set_major_locator(ticker.MaxNLocator(10))
#     ax_main.xaxis.set_major_formatter(ticker.FuncFormatter(x_date))

#     # 메인차트를 그리기
#     ax_main.set_xlabel('Date')
#     ax_main.plot(index, ma20, label='MA20') #20일선 표시
#     ax_main.plot(index, bol_upper, label='bol_upper') #60일선 표시
#     ax_main.plot(index, bol_down, label='bol_down') #60일선 표시
#     ax_main.set_title('HT. S Stock ',fontsize=22) #차트의 Title 설정
#     ax_main.set_xlabel('Date') #차트의 x축 label을 설정
#     #캔들 차트를 실제로 구성하는 부분
#     candlestick2_ohlc(ax_main,ds['Open'],ds['High'],ds['Low'],ds['Close'], width=0.5, colorup='r', colordown='b')

#     ax_main.legend(loc=5) #차트 범례를 오른쪽에 위치하도록 설정
#     plt.grid()
#     plt.show()
