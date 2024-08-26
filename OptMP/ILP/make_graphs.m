%Create the final bar graph

time_array = [5, 10, 30, 180, 300, 420];
score_array = [161.245, 161.215, 156.55, 155.995, 155.985, 155.37];

bar(time_array, score_array, 1.8);
xlabel('Time');
ylabel('Avg. Shortest Path');
title('Avg. Shortest Path vs Time');
grid on;
