export const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
export const pr=(t,s,d)=>cl((t-s)/d);
export const eo=x=>1-Math.pow(1-x,3);
export const eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
export const eob=x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
export function rng(seed=1){return()=>{seed=(seed*16807)%2147483647;return(seed-1)/2147483646}}
export const lerp=(a,b,t)=>a+(b-a)*t;
