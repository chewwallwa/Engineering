clear, clc, close all
% MATLAB cookbook for those who burn ramen by masthierryi - LAMEC (2025)

% variables ===============================================================
variavel1 = 2; % works and ends without printing
variavel2 = 1;  % works (saves the value) and prints the value

a = 1:10; % array
b = 100:100:1000; % from 100 to 1000 in steps of 100
c = [1,2,9,10]; 
d = c'; % transpose
e = [1,2,3,4; 2,3,4,5; 3,4,5,6; 4,5,6,7]; % matrix: ";" creates a new line in the array
f = rand(4,4); % random array 4x4
g = zeros(2,3);
h = ones(3,2);
i = linspace(100,1000,10); % from 0 to 1 in 4 steps
j = size(e); % test size(e,1) and size(e,2)

clear c d g h i j variavel1 variavel2
% array and matrix indexing ===============================================
a(3)
a(5:7)
e(1,:)
e(:,1)
e(:,:)
e
e(2:3,3:4)

% number operations =======================================================
4+2
4-2
4*2
4/2
sqrt(4)
4^-1

disp([sin(pi), cos(pi), tan(pi)]) % the default is radians
disp([rad2deg(pi), deg2rad(180)])
asin(1/2) % asin is arcsin % acos % atan
rad2deg(asin(1/2))

% vector/matrix array operations ==========================================
a + b % must have the same length
e + f
e' + f % " ' " transpose
e*2
e.*[1,2,3,4] % matrix and array, "e." for multiplying each array column by a matrix column
e.*[1,2,3,4]'
e.*f(:,1)'

[e,f] % concatenate horizontally
[e;f] % concatenate vertically
% there are also vertcat(e,f) and horzcat(e,f), with few differences
repmat(e,3,1) % repeat the e matrix by 3x1
% see repelem
diff(b) % (i) element - (i-1) of the array

%{ 
search on web:
logical; isempty; nonzero; ismatrix; string; 
%}

clear, clc
% loops ===================================================================
i = 1;

if i == 1
    ...
elseif i <= 3
    ...
elseif i < 2
elseif i > 2
elseif i >= 2
elseif i ~= 2 % different
elseif i == 2 || i == 3 % it or it
elseif i <= 2 && i == 3 % it and it at the same time
else % none of the previous
end

switch i
    case 2 % i = 2
        ...
    case {1,3} % i = 1 or 3
        ...
    otherwise
end

vec = [];
for k = 1:4 % repeat the loop content 4 times changing k from 1 to 4
    x = k + 1;
    vec = [vec,x];
end

% pre-allocating
vec = zeros(1, 10);  % Vector with 10 elements, all initially zero
% Fill the vector with the desired values
for k = 1:4
    x = k + 1;
    vec(k) = x;  % Assign the value directly in position k
end

clear, clc
% structures ============================================================== 
pessoa.joao.idade = 18;
pessoa.joao.altura = 175;

pessoa.maria.idade = 20;
pessoa.maria.altura = 160;

pessoa.ana.idade = 19;
pessoa.ana.altura = 165;

% Get the field names (people)
pessoas = fieldnames(pessoa);

% Initialize vector to store heights
alturas = [];

% Iterate over each field and collect the height
for i = 1:length(pessoas)
    alturas = [alturas; pessoa.(pessoas{i}).altura];
end

% Calculate the average height
media_altura = mean(alturas);

% Display the result
disp(['The average height is: ', num2str(media_altura)])

clear, clc
% cell ====================================================================
ex = cell(3,1); % pre-allocation

% name, age, height, favorite numbers
dados{1,1} = {'joao',18, 1.75, [2,60]};
dados{2,1} = {'maria',20, 1.60, 7};
dados{3,1} = {'ana',19, 1.665, [3,5,11]};

% Access elements within a cell
aux = vertcat(dados{:,1});
altura_media = mean(cell2mat(aux(:,3)));
disp(['The average height is: ', num2str(altura_media)]);

clear, clc
% plot ====================================================================
x = 1:10;
y = x*2;

plot(x,y,'-o',Color='r')
% search "plot matlab" and look into the plot page on the MathWorks site
% search "types of plots matlab"
