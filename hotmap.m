x=7.5:5:97.5;
y=-0.12:0.02:0.11;
[xx,yy] = meshgrid(x,y);

figure(1);

zz=[];
zz=zz';
% surf(xx,yy,zz);
contourf(xx,yy,zz);
xlabel('�ٶ�(km/h)'),ylabel('���ٶȣ�m/s^2��'),zlabel('Speed(km/h)');
title('���������ʣ�kw/km��','FontName','LucidaSansRegular');
colorbar;

%set(gca, 'XTick', 0:2:24);
%colormap hsv ;
%saveas(gcf, 'Q1', 'tiff')