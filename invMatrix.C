
void invMatrix() {

  TMatrixD M(2,2);
  // BASIC EXAMPLE
  //M(0,0)= 4;
  //M(0,1)= 3;
  //M(1,0)= 3;
  //M(1,1)= 2;
 
  // HORIZONTAL
  //M(0,0)= 0.0863;     
  //M(0,1)= 0.6237;
  //M(1,0)= 0.1059; 
  //M(1,1)= 0.0101; 

  // VERTICAL
  M(0,0)= 0.0801;
  M(0,1)= 0.3593;
  M(1,0)= 0.0670; 
  M(1,1)= 0.0107;

  TMatrixD MI(M);
  MI.Invert(); 

  M.Print();
  MI.Print();

  TMatrixD U(M,TMatrixD::kMult,MI); 

  U.Print();
}

