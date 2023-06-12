from qdrant_tools.vectordb import PineconeExport, QdrantImport, QdrantMode

index_name = "hindi-search"  # Existing Pinecone index name

# Init Pinecone
pinecone_export = PineconeExport(index_name=index_name)
print(pinecone_export.index.describe_index_stats())
source_index = pinecone_export.index

# Fetch all vector ids from Pinecone
vector_ids = ["1", "2", "3", "4", "5"]  # Example vector ids

# Init Qdrant
qdrant = QdrantImport(mode=QdrantMode.local, source_index=source_index)
qdrant.create_collection()
qdrant.upsert_vectors(vector_ids)


qdrant.qdrant_client.search(
    collection_name=index_name,
    query_vector=[
        0.107324339,
        0.171286374,
        -0.025696842,
        0.0255639162,
        -0.200541556,
        -0.298893094,
        0.346795291,
        -0.181934699,
        0.241569281,
        0.499990761,
        -0.600132823,
        0.00091474707,
        -0.120719232,
        0.178959176,
        -0.690440774,
        -0.200460225,
        0.362151176,
        0.228740647,
        -0.117818542,
        0.69618547,
        -0.61137253,
        0.667713523,
        0.113170624,
        0.105125606,
        -0.0467912778,
        -0.18794632,
        -0.217896208,
        0.310907543,
        -0.246946618,
        0.327860981,
        0.396175504,
        0.10662657,
        -0.0699568689,
        0.497462749,
        -0.466855139,
        0.21633172,
        -0.264965475,
        0.43423,
        -0.0392190181,
        0.336269855,
        0.054831963,
        0.188133582,
        -0.186786532,
        -0.164521188,
        0.766651511,
        -0.808231235,
        0.51535058,
        -0.0159842167,
        0.188919768,
        -0.112847976,
        0.00880446564,
        -0.0847014189,
        0.303657293,
        0.0795709714,
        -1.03601444,
        0.179086283,
        -0.414879084,
        0.707882047,
        0.543590188,
        0.0747975409,
        0.207795233,
        -0.267379284,
        0.188594937,
        -0.0266969856,
        0.333730727,
        0.0639132261,
        0.214923516,
        -0.119837992,
        0.475942,
        0.129453838,
        -0.134725943,
        0.210985363,
        0.334220201,
        0.328918457,
        -0.336177021,
        -0.369301528,
        0.033451397,
        0.706461608,
        0.295683891,
        0.102730289,
        0.428735,
        -0.311965466,
        -0.0872216448,
        0.301681519,
        0.395504117,
        0.495979071,
        0.231087968,
        0.138767362,
        0.0194860511,
        0.390014648,
        0.209373727,
        0.122398958,
        -0.344215155,
        -0.447736323,
        0.510537803,
        0.473232388,
        0.299479157,
        -0.234775856,
        -0.0887515321,
        -0.457988381,
        0.156165376,
        -0.338353932,
        -0.662338734,
        0.318918288,
        0.0574952327,
        -0.287984222,
        -0.52294,
        -0.00548449438,
        0.18421559,
        0.293088049,
        0.069747,
        -0.24646689,
        0.128693983,
        0.0225063954,
        -0.414175332,
        -0.0181947052,
        0.672340155,
        0.0996504575,
        -0.0691647083,
        -1.28057671,
        0.272786468,
        -0.0629132,
        -0.208688766,
        0.32963562,
        0.0519430265,
        -0.0630042,
        0.545824468,
        -0.156927973,
        0.496489555,
        0.424453259,
        -0.0602156594,
        0.132492185,
        0.178717762,
        0.505467296,
        -0.47662586,
        -0.215497568,
        -0.202351779,
        0.0683015957,
        -0.326335728,
        -0.370937467,
        -0.117323555,
        0.286621898,
        0.407063335,
        0.900545061,
        -0.0745186731,
        0.0610347949,
        0.195800781,
        0.469776511,
        -0.020233646,
        0.342378557,
        0.370139837,
        0.0114192748,
        -0.370062619,
        0.387657404,
        -0.695187628,
        0.0913064554,
        0.415021479,
        0.0379582755,
        0.406650424,
        0.0688223392,
        0.970666111,
        0.339681,
        0.19670029,
        -0.376337677,
        -0.180637941,
        -0.167101189,
        -0.179441735,
        0.0384492,
        0.278594285,
        0.168786153,
        -0.484574765,
        0.0110651078,
        -0.172208965,
        0.147895351,
        -0.0408830047,
        0.270748705,
        0.497984439,
        0.0572444871,
        0.814335704,
        -0.421785295,
        0.0609133467,
        -0.190298826,
        -0.349602431,
        -0.0493970923,
        0.520611405,
        0.166902483,
        0.217025012,
        0.383606195,
        -0.0684902,
        0.0760876611,
        -0.372646451,
        0.313422471,
        0.542011619,
        -0.42061916,
        -0.0624507,
        0.381156564,
        -0.260479331,
        -0.294048429,
        -0.219103724,
        0.281131625,
        0.35832727,
        -0.787028,
        -0.350986362,
        -0.0298433881,
        0.572687328,
        -0.543445,
        -0.27284193,
        0.383562028,
        -0.199485078,
        -0.127275124,
        -0.0352527052,
        0.0461725742,
        0.480232716,
        0.425373435,
        0.180306345,
        0.224975124,
        -0.178939283,
        0.034531448,
        0.477576047,
        0.159603789,
        -0.0239607785,
        0.240103051,
        -0.0904447362,
        0.255977154,
        0.359249234,
        -0.037167348,
        -0.500403225,
        -0.319063693,
        0.154338434,
        0.514104664,
        0.0467977822,
        0.293264896,
        -0.431805223,
        0.0769788548,
        0.3934955,
        0.439044386,
        0.245484605,
        0.16908145,
        -0.240466952,
        -0.182437643,
        0.692756414,
        0.277030587,
        -0.0223831758,
        -0.414514333,
        0.668297946,
        -0.288158238,
        0.888601601,
        0.0649233535,
        -0.306806147,
        0.439031422,
        0.152745456,
        -0.12290781,
        0.336722523,
        0.613148093,
        -0.184437498,
        0.418952703,
        0.0533657074,
        -0.420075387,
        0.188042551,
        -0.280841261,
        0.21174714,
        0.00635309657,
        0.462676078,
        0.45902,
        0.195674717,
        -0.248086184,
        0.277353913,
        0.381051719,
        0.0905668065,
        0.311672777,
        0.465898931,
        -0.296818763,
        -0.127038434,
        0.225959897,
        -0.327619135,
        -0.245529354,
        0.00368257,
        0.575263739,
        -0.47524932,
        -0.0995910093,
        -0.128638759,
        -0.0806536227,
        -0.137483776,
        0.467451602,
        -0.382857352,
        0.512577653,
        0.156655833,
        -0.24450025,
        -0.298016638,
        -0.347831964,
        0.150107637,
        0.614165306,
        -0.144901127,
        0.0342038758,
        0.330572635,
        0.54896313,
        0.0786267519,
        -0.0190345012,
        0.371284246,
        0.00504353549,
        0.347387433,
        -0.213220775,
        0.15494746,
        0.844463944,
        -0.0244069099,
        -0.811123908,
        -0.0694730356,
        -0.168866411,
        0.183655947,
        0.197744131,
        0.171859205,
        -0.782274663,
        -0.31987232,
        0.251383,
        0.399323434,
        1.29949391,
        0.0435856171,
        0.0358654857,
        0.203603804,
        0.140791222,
        -0.0480151772,
        -0.0374785773,
        -0.353039145,
        0.442153931,
        0.063450411,
        -0.227846086,
        -0.0501569696,
        -0.579108953,
        0.987944603,
        0.515784085,
        0.237158343,
        0.0358586758,
        -0.334674031,
        -0.0478792749,
        -0.0962414294,
        0.23815085,
        -0.0167955626,
        0.826010942,
        -0.327320099,
        0.654602051,
        0.271441847,
        0.351160228,
        0.360675246,
        0.196624473,
        0.0155596007,
        0.354240656,
        -0.2221791,
        0.374674469,
        -0.0735253841,
        -0.00898132939,
        0.422661513,
        0.193652824,
        0.382943809,
        0.223275855,
        0.115163632,
        -0.00993324071,
        0.370844394,
        0.303065568,
        0.839577436,
        -0.222350612,
        0.540103793,
        0.743892789,
        0.335514873,
        -0.0442226157,
        0.417904019,
        0.156825215,
        0.179742828,
        -0.39050293,
        0.182001114,
        0.189076826,
        0.809818149,
        -0.419875175,
        -0.570983887,
        0.285785556,
        -0.0150121627,
        -0.189499244,
        -0.137719676,
        0.577656507,
        0.315974385,
        0.304870963,
        0.369430065,
        0.738277555,
        0.237401783,
        -0.100471146,
        -0.256407291,
        -0.0965313166,
        -0.137645438,
        0.474627048,
        -0.192850009,
        -0.388780534,
        -0.326317519,
        -0.0905805156,
        0.399474174,
        0.169966593,
        -0.604764044,
        0.161335334,
        -0.253958166,
        0.382138789,
        0.462002844,
        -0.0207487736,
        -0.0528231673,
        0.623316884,
        0.393336445,
        0.702932656,
        4.17631388,
        -0.0419399962,
        0.324855685,
        0.546198547,
        0.0626485422,
        -0.0214873236,
        0.679984331,
        -0.73269558,
        0.288672239,
        -0.0932773277,
        -0.447963834,
        0.0042287074,
        -0.0141949216,
        0.0924526304,
        0.426000416,
        -0.0851609185,
        0.232479274,
        -0.083586894,
        -0.0317552723,
        0.335429579,
        -0.367547244,
        -0.480008453,
        0.285704643,
        -0.132633328,
        0.568165183,
        0.22993423,
        -0.04525,
        0.810242653,
        0.523572505,
        0.0581575297,
        0.532112837,
        -0.150981322,
        0.253057659,
        -0.0996136516,
        -0.141557112,
        0.967988,
        0.0980324298,
        0.324512184,
        0.1060917,
        -0.0124734528,
        -0.240806118,
        -0.0072711329,
        -0.22154054,
        0.424209118,
        0.339700401,
        -0.507429659,
        0.177005157,
        0.608908892,
        0.214520454,
        0.213441119,
        0.0840399042,
        -0.303364605,
        -0.27082178,
        -0.307916224,
        -0.276508689,
        0.543508828,
        0.0338980444,
        0.050850492,
        0.571289062,
        -0.0193310361,
        0.248252407,
        -0.00110666314,
        0.560759544,
        0.0949706733,
        -0.295481145,
        -0.0856782198,
        -0.383552313,
        0.114501432,
        0.55100137,
        -0.328389943,
        0.139321178,
        0.247343123,
        0.107730053,
        -0.559618413,
        -0.372124195,
        0.307760537,
        -0.462560594,
        -0.432784349,
        -0.197626397,
        -0.267934173,
        0.00533512142,
        0.0546546131,
        -0.231782854,
        -0.0124247,
        0.0199233554,
        0.517041743,
        -0.0498915315,
        -0.139110446,
        0.551015198,
        0.324400365,
        0.114495739,
        -0.347706407,
        0.5679636,
        0.342475027,
        -0.21162276,
        0.482444078,
        -0.524490356,
        -3.93033862,
        0.208318308,
        0.304401159,
        -0.0695229471,
        0.222899467,
        -0.0097688036,
        -0.24270387,
        0.0539106689,
        -0.114133202,
        -0.159176424,
        0.11731685,
        0.203933254,
        -0.227299541,
        0.064946264,
        -0.0912546,
        -0.0101802275,
        0.258642137,
        0.359210402,
        0.272382319,
        0.0162399746,
        0.716560125,
        0.262913555,
        0.117134005,
        0.253862381,
        0.198417783,
        0.20821242,
        0.394212425,
        0.0834388584,
        -0.165191069,
        0.181082055,
        -0.156871915,
        0.491912365,
        0.47153911,
        0.146401569,
        0.585756242,
        0.713082969,
        0.261800826,
        -0.171583921,
        0.0268730391,
        0.251654088,
        -0.130965605,
        -0.318659,
        0.261617035,
        0.175946206,
        -0.159536883,
        0.0403011777,
        -0.117100358,
        -0.0983383879,
        -0.34312138,
        0.223438784,
        -0.133892298,
        0.0200713184,
        -0.500157237,
        -0.214812174,
        0.35171786,
        0.145558298,
        0.116832271,
        -0.127321452,
        0.142068475,
        0.309954107,
        0.379271775,
        -0.051140178,
        0.293365359,
        0.10931547,
        -0.187175632,
        -0.164074644,
        0.495451957,
        0.189469576,
        -0.0591894872,
        -0.321674585,
        0.0687276646,
        0.266899347,
        0.294001728,
        -0.149105772,
        0.352303714,
        0.310437292,
        -0.191265568,
        0.0593763106,
        0.536684,
        -0.0869262,
        -0.339512676,
        0.0901970118,
        -0.419945925,
        0.02271083,
        2.0218246,
        0.506303251,
        2.08459091,
        0.234618902,
        0.0407378748,
        0.278149217,
        0.137524977,
        0.278686523,
        0.388481379,
        -0.277044922,
        -0.381740689,
        -0.139717683,
        -0.175039813,
        0.0623970889,
        0.0477364585,
        -0.354908347,
        0.516442478,
        -1.29287994,
        -0.0230387915,
        -0.482946455,
        0.501760781,
        0.00752385473,
        -0.294012368,
        0.235648185,
        -0.00850079302,
        0.194470033,
        0.408102334,
        -0.0694545135,
        -0.148941621,
        -0.433661,
        0.0974689797,
        -0.313787401,
        0.317736089,
        0.0757423192,
        -0.0414291732,
        0.33427754,
        -0.0484857559,
        4.53284788,
        0.154542282,
        -0.0101950606,
        0.252738714,
        0.485719621,
        0.0193423182,
        0.526825905,
        0.0882720426,
        0.198967785,
        -0.0103678564,
        0.387825936,
        0.610673368,
        0.336525649,
        -0.163342789,
        0.216220617,
        -0.0800164565,
        0.182416856,
        0.364088565,
        0.0227778908,
        0.0167279821,
        -0.217800841,
        -0.00205184473,
        -0.16172421,
        -0.0549679659,
        0.186030298,
        0.200377494,
        0.134034768,
        0.338170141,
        -0.097067,
        -0.522726834,
        0.162585154,
        5.22165,
        -0.00203577685,
        -0.346483976,
        -0.25399375,
        -0.161676586,
        0.404905617,
        -0.343733341,
        -0.0151083972,
        -0.0859789401,
        -0.00883342326,
        0.031373024,
        0.34676984,
        0.152848735,
        0.38318,
        0.561713934,
        0.0270612314,
        -0.367672086,
        -0.253510445,
        0.191463783,
        -0.169825643,
        0.609680891,
        0.33464098,
        0.313978702,
        -0.450356215,
        0.0673497543,
        -0.165853322,
        -0.404004633,
        0.148052454,
        0.00688463449,
        -0.292937309,
        0.374206543,
        0.838112593,
        -0.347521245,
        0.288279206,
        -0.459074527,
        -0.35336107,
        -0.048999209,
        -0.106357776,
        0.0238309912,
        -0.0496458,
        0.254422039,
        0.791063726,
        -0.106263593,
        -0.341456622,
        -0.250495225,
        0.452694058,
        -0.157721892,
        0.660404086,
        0.327751398,
        0.0859299898,
        0.451859921,
        0.0454293452,
        0.887841403,
        0.0564196557,
        0.297466636,
        -0.0535673089,
        0.129176423,
        -0.20504114,
        -0.150076777,
        -0.0509194881,
        0.507917523,
        0.0120598255,
        -0.0116771348,
        0.385826349,
        0.278707802,
        0.423203,
        0.132227749,
        0.0109257121,
        0.941258311,
        0.225554153,
        -0.0609650537,
        0.421039462,
        -0.0332426876,
        0.660328746,
        0.243564025,
        0.414981723,
        0.54398787,
        0.437466711,
        0.385354817,
        0.265253693,
        -0.114073768,
        -0.817745328,
        -0.512369812,
        0.118049264,
        0.107581541,
        -0.0309381783,
        0.0117457993,
        -0.155530989,
        0.219643801,
        -0.187082469,
        0.227861583,
        -0.882612765,
        0.27668485,
        -0.0329261683,
        0.153258711,
        -0.393071949,
        -0.302574396,
        0.0266664103,
        -0.302352428,
        0.0501501337,
        -0.344298631,
        0.353061318,
        -0.153211072,
        0.396907,
        0.122239731,
        -0.216141447,
        -0.0216978826,
        0.180006295,
        0.1504886,
        0.105999976,
        0.423661679,
        0.611354589,
        -0.149057269,
        -0.196108371,
        -0.104151219,
    ],
)
