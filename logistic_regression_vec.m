function [f,g] = logistic_regression_vec(theta, X,y)
f=log(h_theta(theta,X))*y'+log(1-h_theta(theta,X))*(1-y)';
f=-f;
Xt=h_theta(theta,X)-y;
g=X*Xt';
end