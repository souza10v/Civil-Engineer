################################################################################

################################################################################
# FEDERAL UNIVERSITY OF CATALÃO (UFCAT) - BRAZIL
# DEVELOPERS:
# souza10v
# GITHUB: github.com/souza10v
# LICENSE: Free academic
################################################################################

################################################################################
# DESCRIPTION SCRIPT:

# Verification of a metallic beam in section I according to the Brazilian Standard Code NBR 8800 - 2008
################################################################################

################################################################################

def FLANGE_LOCAL_BUCKLING(BF,TF,YOUNG_MODULUS,FY):  #Flambagem local na mesa FLB. Considerando aços de maneira geral conforme NBR 8800. Portanto type1=3 não atingindo.
  LAMBDA=BF/(2*TF)     
  LAMBDAP=0.38*((YOUNG_MODULUS/FY)**0.5)  
  LAMBDAR=(YOUNG_MODULUS/FY)**0.5   
  if LAMBDA <= LAMBDAP:
    TYPE1=1    #"COMPACT SECTION"
  elif LAMBDA>LAMBDAP and LAMBDA<=LAMBDAR:
    TYPE1=2    #"NON COMPACT SECTION"
  else:
    TYPE1=3     #"SLENDER SECTION"
  return (TYPE1)

def WEB_LOCAL_BUCKLING(HW,TW,YOUNG_MODULUS,FY): #Flambagem local na alma FLB. Considerando aços de maneira geral conforme NBR 8800. Portanto type1=3 não atingindo.
  LAMBDA=HW/TW    
  LAMBDAP=3.76*((YOUNG_MODULUS/FY)**0.5)    
  LAMBDAR=5.7*((YOUNG_MODULUS/FY)**0.5)   
  if LAMBDA<=LAMBDAP:
    TYPE2=4    #"COMPACT SECTION"
  elif LAMBDA>LAMBDAP and LAMBDA<=LAMBDAR:
    TYPE2=5    #"NON COMPACT SECTION"
  else:
    TYPE2=6    #"SLENDER SECTION"
  return (TYPE2)
  
def SETION_DEFINITION(TYPE1,TYPE2): #type1=3 não atingindo. Portanto não está aqui.
  if TYPE1==1 and TYPE2==4:
    TYPE_BEAM=TYPE1 #Compact #1
    print("Compact")
  elif TYPE1==2 and TYPE2==4: #2
    TYPE_BEAM=2 #Non compact due the flange
    print("Non compact due the flange")
  elif TYPE1==1 and TYPE2==5: #5
    TYPE_BEAM=TYPE2  #Non Compact due web
    print("Non Compact due web")
  elif TYPE1==2 and TYPE2==5: # 2 E 5, equal 7
    TYPE_BEAM=7  #Non compact due the flange and web
    print("Non compact due the flange and web")  
  return (TYPE_BEAM)

def RESISTANT_DESIGN_MOMENT(TYPE_BEAM,GAMMAA1,FY,Z,REQUESTING_BENDING_MOMENT,BF,TF,E): 
  if TYPE_BEAM ==1: #COMPACT 
    momentoresistentciaplastico=Z*FY 
    RESISTANT_DESIGN_MOMENT=momentoresistentciaplastico/(GAMMAA1*100)
    if REQUESTING_BENDING_MOMENT<RESISTANT_DESIGN_MOMENT: #profile check
      print("Mrs<Mrd")
    else:
      print("Change section.")
  elif TYPE_BEAM==2:  #Non Compact due flange
    LAMBDA=BF/2*TF    
    LAMBDAP=0.38*((E/FY)**0.5)    
    LAMBDAR=(E/FY)**0.5    
    momentoresistentciaplastico=Z*fy
    momentoresistenciaelastico=W*FY 
    RESISTANT_DESIGN_MOMENT=(momentoresistentciaplastico-(momentoresistentciaplastico-0.7*momentoresistenciaelastico)*((LAMBDA-LAMBDAP)/(LAMBDAR-LAMBDAP)))/GAMMAA1
    if REQUESTING_BENDING_MOMENT<RESISTANT_DESIGN_MOMENT: #profile check
      print("Mrs<Mrd")
    else:
      print("Change section.")
  elif TYPE_BEAM==5:  #Non Compact due web
    LAMBDA=H/TW     
    LAMBDAP=3.76*((E/FY)**0.5)    
    LAMBDAR=5.7*((E/FY)**0.5)   
    momentoresistentciaplastico=Z*FY 
    momentoresistenciaelastico=W*FY 
    RESISTANT_DESIGN_MOMENT=(momentoresistentciaplastico-(momentoresistentciaplastico-0.7*momentoresistenciaelastico)*((LAMBDA-LAMBDAP)/(LAMBDAR-LAMBDAP)))/GAMMAA1
    if REQUESTING_BENDING_MOMENT<RESISTANT_DESIGN_MOMENT: #profile check
      print("Mrs<Mrd")
    else:
      print("Change section.")
  elif TYPE_BEAM==7:  #Non compact due the flange and web
    print("Error")
  return (RESISTANT_DESIGN_MOMENT)

def SECTIONS_CLASSIFICATION(HW,TW,YOUNG_MODULUS,FY):
    LAMBDA=HW/TW     
    LAMBDAP=2.46*((YOUNG_MODULUS/FY)**0.5)
    LAMBDAR=3.06*((YOUNG_MODULUS/FY)**0.5)
    if LAMBDA <= LAMBDAP:
      CV=1
      #print(f"CV={CV} ")
    elif LAMBDAP<LAMBDA and LAMBDA<=LAMBDAR:
      CV=(2.46/(HW/TW))*((YOUNG_MODULUS/FY)**0.5)
      #print(f"CV={CV} ")
    elif LAMBDA>LAMBDAR:
      CV=(7.5*YOUNG_MODULUS)/(FY*((HW/TW)**2))
      #print(f"CV={CV} ")
    return (CV)

def RESISTANT_DESIGN_SHEAR(CV,FY,AW,GAMMAA1,REQUESTING_SHEAR_FORCE):
  VRD=(CV*0.6*FY*AW)/(GAMMAA1)
  if REQUESTING_SHEAR_FORCE<VRD:
    print("Vrs<Vrd")
  else:
    print("Change section.")
  return (VRD)

def MAX_DEFLETION(LENGTH,TYPE_BEAM):
  LENGTH_C=LENGTH*100 #cm
  if TYPE_BEAM == 1:
    MD=LENGTH_C/250
  elif TYPE_BEAM == 2:
    MD=LENGTH_C/350
  elif TYPE_BEAM == 3:
    MD=LENGTH_C/500
  else:
    print("Type Beam Error")
  return (MD)

def REQUESTED_DEFLEXTION(MAX_DEFLETION,REQUISTING_LOAD,LENGTH,YOUNG_MODULUS,INERTIA,BEAM_CONDITION):
  LENGTH_C=LENGTH*100 #cm
  REQUISTING_LOAD_C=REQUISTING_LOAD/100 #kN/cm
  YOUNG_MODULUS=YOUNG_MODULUS #kN/cm^2
  if BEAM_CONDITION == 1:
    RD=(REQUISTING_LOAD_C*LENGTH_C**4)/(384*YOUNG_MODULUS*INERTIA)
  elif BEAM_CONDITION == 2:
    RD=(5*REQUISTING_LOAD_C*LENGTH_C**4)/(384*YOUNG_MODULUS*INERTIA)
  else:
    print("Beam Condition Error")
  if RD <= MAX_DEFLETION:
    print("SD<SMAX")
  else:
    print("Change.")
  return (RD)

###################################################
# STEP 1: BEAM DATASET
###################################################
print("Verification of a metallic beam in section I according to the Brazilian Standard Code NBR 8800 - 2008")
print("Verificação de uma viga métalica em perfil I sujeita a Normativa Brasileira NBR 8800 - 2008.")

print(" ")
# 1.1: EXTERNAL LOADS: MEAN VALUES
requestingBendingMoment=float(input("Insert the bending moment [MSD(kN.m)]: "))

# 1.2: MATERIAL PROPERTIES
youngModulus=float(input("Insert the elasticity modulus for steel [E(kN.cm^2)]: ")) 
fy=float(input("Insert the flow resistance [fy(kN/cm^2)]: ")) 
z=float(input("Insert the plastic section modulus [Z(cm^3)]: "))

# 1.3: SECTION PROPERTIES #W 150 x 18.0
length=float(input("Insert the length beam [L(m)]: ")) 
h=float(input("Insert the height section total [h(mm)]: "))
bf=float(input("Insert the width of flange [bf(mm)]:"))
tf=float(input("Insert the thickness of flange [tf(mm)]:"))
hw=float(input("Insert the width of web [hw(mm)]:"))
tw=float(input("Insert thethickness of web [tw or to(mm)]:"))
inertia=float(1input("Insert the moment of inertia [I(cm^4)]: ")) 
print(" ")

# 1.4: LOAD FACTORS
gammaA1=1.1  #load factor gammaa1

# 1.5: REQUESTED EFFORTS

requestingLoad=(requestingBendingMoment)*8/(length**2) 
requestingShearForce=(requestingLoad*length)/2 

#1.6: ADITIONAL INFO

beamCondition=2 #1 Cantilever, 2 Simply suppoterd  
typeBeam=2  #1 viga de cobertura, 2 vigas de piso, 3 vigas que suportam lajes

###################################################
#STEP 2: BEDING MOMENT
###################################################

# 2.1: CLASSIFICATION OF THE SECTIONS 
print("Section type: ")
flbType=FLANGE_LOCAL_BUCKLING(bf,tf,youngModulus,fy) 
wlbType=WEB_LOCAL_BUCKLING(hw,tw,youngModulus,fy) 
type_beam=SETION_DEFINITION(flbType,wlbType) 
print("")

# 2.2: MOMENT RESISTED BY THE SECTION 
mrd=RESISTANT_DESIGN_MOMENT(type_beam,gammaA1,fy,z,requestingBendingMoment,bf,tf,youngModulus) 
print(f"MRD {mrd:.2f} e MSD  {requestingBendingMoment:.2f} {(requestingBendingMoment/mrd)*100:.2f}%")
print(" ")

###################################################
#STEP 3: SHEAR FORCE
###################################################

# 3.1: CLASSIFICATION OF THE SECTIONS 
cv=SECTIONS_CLASSIFICATION(hw,tw,youngModulus,fy) 
aw=h*tw*0.01 #effective area

# 3.2 SHEAR RESISTED BY THE SECTION 
vrd=RESISTANT_DESIGN_SHEAR(cv,fy,aw,gammaA1,requestingShearForce)
print(f"VRD {vrd:.2f} e VRS  {requestingShearForce:.2f} {((requestingShearForce/vrd)*100):.2f}%")
print(" ")

###################################################
#STEP 4: VERTICAL DEFLECTIONS
###################################################

#4.1: MAX SUPPORTED DEFLEXTION
maxDeflection=MAX_DEFLETION(length,typeBeam)

#4.2 REQUESTED DEFLEXTION 
requestedDeflexition=REQUESTED_DEFLEXTION(maxDeflection,requestingLoad,length,youngModulus,inertia,beamCondition)
print(f"SMAX {maxDeflection:.2f} e SD  {requestedDeflexition:.2f} {(requestedDeflexition/maxDeflection)*100:.2f}%")
print(" ")