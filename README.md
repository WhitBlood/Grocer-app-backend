Grocery Store - A roducion-radyst with support for both local development and AWS RDS Aurora PostgreSQL deployment�Featues

- **User Management**: Registratin, authntiaion,JWT okens
- **Pod Catalog**: Categois, produts with ratigs an reviews-**ShoingCart&Orders**:Full order maagemen sstem
-**AddressManagement**:Multipledeliveryaddressesperuser
-**AWSReady**:SeamlessdeploymenttoAWSRDSAuror
- **DorSupport**: Coanerd fo easy deployment- **Health Checks**:Built-inhealthandredness edoints
- **CORS Configured**: Read forfrontendintegration

##📋Prerequisites

-Python3.12+
-PostgreSQL15+(local)orAWSRDSAuroraPostgreSQL
-Docker(optional,forcontainerizeddatabe)
- WS CL (for AWSdeoyment)

## 🏃 Quk Start

### 1. Clone nd Seup

```bash
gt clone <your-repo>
cd Grocer-app-backend
pythn -m venv vevsourcevenv/bin/activate#Winows: venv\Scripts\civt
piinstall-rrequirements.txt
```

###2.ConfigureEnvironment

```bash
cp.env.example.env
#Edit.envwithyourconfiguration
```

###3. Start

**Option A:Doker**
```bash
dcker ru --ame frshmar-pstgres \-ePOSTGRES_USER=to_usr \
 -ePOSTGRES_PASSWORD=ams123\
-ePOSTGRES_DB=freshmart_db\
-p5432:5432\
-dpostgres:15
```

**OptionB:LocalPostgre**
```bash
sudo servipstgrsq tartsudo-upotgr sql -c"CREATEUSERtodo_userWITHPASSWORD'ams123';"
sudo-upostgrespsql-c"CREATEDATABASEfreshmart_dbOWNERtodo_user;"
```

##4. IializeDatabae

```bas
python rcrete_table.py```

###5.RunAppliati

```bash
uvcorn appmain:ap --reload
```

Visit:
-API:http://localhost:8000
-Docs:http://localhost:8000/docs
-Health:http://localhost:8000/health

##🌐AWSDeployment

ForAWSRDSAuroraPostgreSQLdeployment,see[docs/AWS_DEPLOYMENT.md](docs/AWS_DEPLOYMENT.md)

## Quick AWS Setup

1. **Setenvirnmet varables**
   ```bash
   export USE_AWS_SECRETS=tre
   expot AWS_REGION=us-es-1
   exprtAWS_SECRET_NAME=rd-db-password
   ```

2. **Crae AWS Secre**
   ```bahawsscrtsmaagr rate-ecret\
--namerds-db-password\
  --scret-string '{
       "ernm":"frshmart_admi",
       "passwor": "your-password",
       "host": "your-clustr.lustr-xxxxx.u-east-1.rds.amazonaws.com","pr": 5432,
       "dbnam": "fehmart_db",
"SECRET_KEY":"your-jwt-secret"
}'
```

3.**Deploy application** (EC2, ECS, or Lambda)

# 📁rojectStructure

```
Grocer-app-back/
├── ap/
│   ├── ruer/      #APIroutehadlerson endpits├Utiity#JWT&phashng   configpy#Configurationmanagement
│├──database.pyDtasonncon│   modlsySQLAchmymds│   schapy    #Pydanticschemas
│├──dependencies.pyFastAI│   └maAppc entry pointocs/Documn│   WS_DPLOYMET.md
│   ├── ATABASESCHMA
│└──...
├──.env.example  Envirnent tema
├──.ignorerequireents.txtPythn dendncsockerfile     nainrfiniionADM       Thifl�ConfguaionEnvionmnVrils| Vile| Dcipion|Dful||----------|-------------|---------||USE_AWS_SECRETS|UsAWSSMagr|fals || ` | PSQL cnntin ing | Rquie || `` | JWT   | Rqured || `VONM` | nvironment name | `development` || `S` | COR alwed rigin | `000` || LOG_LEVEL|Loggig vl | `INFO` || SQL_ECHO|LogSQL ei|`ru|See[ev.exmp](.vxmp)forcoefguiooin.�Proucts
- `GET /poduct/` - Lit all productprouct{id}t producdetis
- `GET/prodct/category/{catgory_id}` - Poductsby ctegory

### Ores
- `GET /ordr/` - Lit uerododrore
- `GET /ordr/{id}`- Get od dtail

###AddressesLisures
-`POST /addss/`- Add new ddress

###HlGE` - Bc hhcheck
`GET/hh`-Dtaldhelstatready` - Readiness be

Full API ocmentation: http://loalhos:8000/doc

##🗄️DatabasSchem

Theaplicatin seeollowng tab: **users**-Use accn
- **user_adresses**Dliveryaddress
- **ategores**- P categories**** - Produt calo
- **ders** - Custororders
**ordr_iems**- Oder line items

See [dcs/DATABASE_SCHEMA.m](do/DATABASE_SCHEMA.md)fordeaild schema.

## 🐳 DckeBuil Imag``bash
ockbuild tfshmr-api.
```

### RuCntaine
```bash
ockn -d \
  --name fhmr-api \  p8000:8000\
  --nv-file .env \
  fehmart-api
``

##🧪Tsing

```bash
#Rn test
pytst

# Withcveage
pytt --cov=apptsts/
```

## 📊 Montoing

### Hlh Cecks
 **Liveness**:halthRurns 200 app sunning
-**Radns**:GEeay` - Rtun 200 f atabase is onetd

### Logging

Appicationlogsiu:
-Rest/espons log
-Databse qery logs (when `SQL_ECHO=rue`-Errortrac
- Healh checksul## 🔒 ScuJWT-bad uthntictohshg with bcrypt- ORS prtctionSQL injction pevetion (SQLAlchmyORM)
- Envirment-base scretsAWS Secret Manageintegrtin�-[AWSDeoymnG](ocs/WSDELYMN)
[Schma](docs/DATASSCHMA)
[HalhChek Gid](doc/HELTHHCK)
[Stu Checkls](doc/ST_CHECKLISx)🤝tributig1.Fok herository
2. Craea fatu banh
3. Make yuchnges
4 Subt  ullquest#📝Lene
MIT Lese

##🆘Tublesing##DCIssu```bash
T cecio
ockr x -t frhmart-ogres psqU todo_use-d fshar_dbif daabasi rnningdocker s | rep potgs#AWSSecsaageIsss```bash
#Testseretievalwseetsgergetsect-vae--ser-idrds--psword# IAMpemsos
awsmgt-ole-polc--rol-ameYoRol--poly-nmYouPolicy
``Applicatio Wn'Start1. hckexssandha corrctus2.Verifydiunningccibl3.hck los frr4.Ensuealldepenenieinsle:`pipinall-quit.txt`�ppoForiuenqss:Chck[oc/]dos/) fdrevwerl-Chckatabasencvty---Bilwih ❤️sngFaPadPosgSQL