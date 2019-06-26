x=7.5:5:97.5;
y=-0.12:0.02:0.11;
[xx,yy] = meshgrid(x,y);

figure(1);

zz=[];
zz=zz';
% surf(xx,yy,zz);
contourf(xx,yy,zz);
xlabel('速度(km/h)'),ylabel('加速度（m/s^2）'),zlabel('Speed(km/h)');
title('能量消耗率（kw/km）','FontName','LucidaSansRegular');
colorbar;

%set(gca, 'XTick', 0:2:24);
%colormap hsv ;
%saveas(gcf, 'Q1', 'tiff')