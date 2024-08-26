% Read data from files
nodesData = importdata('Nodes2.txt');
linksData = importdata('Links2.txt');
costData = importdata('L2.txt');

% Extract node information
numNodes = size(nodesData, 1);

% Parameters
n = 10;               % Number of switches to select
Cmax = 1000;          % Maximum shortest path length


% Create cost matrix
% Check if the costMatrix file already exists
if exist('costMatrix.mat', 'file') == 2
    % If the file exists, load the costMatrix from the file
    load('costMatrix.mat');
else
    % Create cost matrix
    costMatrix = zeros(numNodes, numNodes);
    for i = 1:size(linksData, 1)
        fromNode = linksData(i, 1);
        toNode = linksData(i, 2);
        cost = costData(fromNode, toNode);

            costMatrix(fromNode, toNode) = cost;
            costMatrix(toNode, fromNode) = cost;
       
    end

    % Save the costMatrix to a file
    save('costMatrix.mat', 'costMatrix');
end

%Create graph
G = graph(costMatrix);

%Not actually shortestpath 
if exist('shortestpathMatrix.mat', 'file') == 2
    % If the file exists, load the shortestpathMatrix from the file
    load('shortestpathMatrix.mat');

else
    % Cell array to store all paths
    getShortestPaths = zeros(numNodes, numNodes);
    % Function to find paths using distances function
    for i=1:numNodes
        for j=1:numNodes
            getShortestPaths(i,j) = distances(G, i,j);

        end
    end
    save('shortestpathMatrix.mat', 'getShortestPaths');
end

% Open the LPSolve input file for writing
fid = fopen('Final_Output.lpt', 'w');

% Objective function
fprintf(fid, 'Minimize\n obj:');
for i = 1:numNodes
    for j=1:numNodes
        if i ==1 && j ==1
            fprintf(fid, ' %d g%d_%d ', getShortestPaths(i,j),i,j);
        else
            fprintf(fid, ' + %d g%d_%d ', getShortestPaths(i,j),i,j);
        end
    end
end
fprintf(fid, '\nSubject to\n');

countconstraints=1;


% Constraints: Select n nodes as controllers
fprintf(fid,' c%d: ',countconstraints);
for i = 1:numNodes
    if i==1
        fprintf(fid, 'x%d ', i);

    else
        fprintf(fid, '+ x%d ', i);

    end
end
fprintf(fid, '= %d\n', n);

%Constraint 2
for i = 1:numNodes
    countconstraints =countconstraints+1;

    fprintf(fid,' c%d: ',countconstraints);
        for j = 1:numNodes
           if j ==1
            fprintf(fid,'g%d_%d ',j,i );
           else
            fprintf(fid,'+ g%d_%d ',j,i );
           end
        end
    fprintf(fid,'= 1 \n');
end

% Constraint 3:
countconstraints =countconstraints+1;
for i = 1:numNodes
    for j =1:numNodes
        fprintf(fid, ' c%d: g%d_%d - x%d <=0\n', countconstraints,i,j,i);
        countconstraints =countconstraints+1;
    end
end

%Cmax constraint
for i = 1:numNodes
    for j =1:numNodes
        if getShortestPaths(i,j)>Cmax
            fprintf(fid,' c%d: x%d + x%d <= 1\n',countconstraints,i,j);
            countconstraints =countconstraints+1;

        end
    end
end

%Binary
fprintf(fid,'Binary\n');
for i=1:numNodes
    fprintf(fid,' x%d',i);
end
for i = 1:numNodes
    for j =1:numNodes
        fprintf(fid,' g%d_%d',i,j);

    end
end

% End the LPSolve input file
fprintf(fid, '\nend\n');

% Close the file
fclose(fid);
