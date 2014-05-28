
void invMatrix() {

  TMatrixD M(2,2);
  // BASIC EXAMPLE
  //M(0,0)= 4;
  //M(0,1)= 3;
  //M(1,0)= 3;
  //M(1,1)= 2;
 
  // HORIZONTAL
  //M(0,0)= 0.0863;     
  //M(0,1)= 0.6205;
  //M(1,0)= 0.1059; 
  //M(1,1)= 0.0114; 

  // VERTICAL
  M(0,0)= 0.0670;
  M(0,1)= 0.3560;
  M(1,0)= 0.0801; 
  M(1,1)= 0.0120;

  TMatrixD MI(M);
  MI.Invert(); 

  M.Print();
  MI.Print();

  TMatrixD U(M,TMatrixD::kMult,MI); 

  U.Print();
}

