from tweets.models import TweetNode
from tweets.services.embedding import Embedding

class Candidates:
    def __init__(self, user_id):
        self.user_id = user_id 
        self.embedding = Embedding()  
        self.tweets = None
        self.tweet_id_to_tweetNode_map = None
        self.list_of_vector_embeddings_maps = None
        self.recommendation_vector_embedding = None
    
    def get_all_tweets_with_embeddings(self):
        self.recommendation_vector_embedding = self.get_personal_recommendation_vector_embedding()
        self.list_of_vector_embeddings_maps = self.embedding.query_vector_embeddings(self.recommendation_vector_embedding)
        self.tweet_id_to_tweetNode_map = self.get_corresponding_tweets_for_vector_embeddings()
        self.all_tweets_with_embeddings = self.build_tweet_node_and_embeddings_doc()
        return self.all_tweets_with_embeddings
    
    def get_corresponding_tweets_for_vector_embeddings(self):
        list_of_tweet_id = []
        for vector_embedding_dict in self.list_of_vector_embeddings_maps:
            list_of_tweet_id.append(vector_embedding_dict["id"])
        
        self.tweets = TweetNode.objects.filter(id__in = list_of_tweet_id)
        tweet_id_to_tweetNode_map = {}
        for tweet in self.tweets:
            tweet_id_to_tweetNode_map[str(tweet.id)] = tweet
        
        return tweet_id_to_tweetNode_map
    
    #this will be replaced later with embedding space, a class that will handle all embedding related operations
    def get_personal_recommendation_vector_embedding(self): 
        return self.get_temp_embedding()
    
    
    def build_tweet_node_and_embeddings_doc(self):
        '''
        
        Returns: 
        tweet_node_and_embeddings_doc: A list of dictionary where each dictionary is -
                                composed of unique tweetnode(tweetNode) and the vector embedding(embedding) associated to the tweet
        
        [
            {   
                "tweet_node": <TweetNode Object>
                "embedding: {
                                'id': 'tweet-id1',
                                'metadata': {'text': 'The tech company Apple is known for its '
                                                    'innovative products like the iPhone.'},
                                'score': 0.8727808,
                                'sparse_values': {'indices': [], 'values': []},
                                'values': [-0.006929283495992422,-0.005336422007530928, -4.547132266452536e-05,-0.024047505110502243]
                            }
            }, 
            
            {
                "tweet_node": <TweetNode Object>
                "embedding: {
                                'id': 'tweet-id2',
                                'metadata': {'text': 'Apple Inc. has revolutionized the tech '
                                                    'industry with its sleek designs and '
                                                    'user-friendly interfaces'},
                                'score': 0.8727808,
                                'sparse_values': {'indices': [], 'values': []},
                                'values': [-0.006929283495992422,-0.005336422007530928, -4.547132266452536e-05,-0.024047505110502243]
                            }
            }
        ] 
        
       '''
       
        list_of_maps = []
        tweet_node_embedding_map = {}
        for vector_embedding_map in self.list_of_vector_embeddings_maps:
            tweet_node_embedding_map = {}
            tweet_id = vector_embedding_map["id"]
            tweet_node_embedding_map["tweet_node"] = self.tweet_id_to_tweetNode_map[tweet_id]
            tweet_node_embedding_map["embedding"] = vector_embedding_map
            list_of_maps.append(tweet_node_embedding_map)
        return list_of_maps   
    
    def get_temp_embedding(self):
        temp_embedding = [-0.003471853444352746, 0.012083767913281918, -0.03956129029393196, 0.07225155085325241, 0.04606234282255173, -0.06141645833849907, 0.022502630949020386, 0.057716671377420425, 0.03467228636145592, -0.05073993280529976, 0.0019010957330465317, -0.006084827706217766, -0.03813422843813896, 0.0020778265316039324, -0.01005549170076847, -0.05142703652381897, -0.03126319870352745, -0.02451108582317829, 0.012876578606665134, -0.02620241791009903, -0.013966694474220276, 0.00025890249526128173, 0.018128953874111176, 0.002176928101107478, 0.00672238040715456, -0.028012670576572418, -0.04170188307762146, 0.037103574723005295, -0.04931287094950676, -0.002713727531954646, 0.011773250065743923, -0.03239956125617027, 0.0027665814850479364, -0.02420717477798462, 0.010280121117830276, 0.009824254550039768, 0.043049659579992294, 0.000156084744958207, 0.016754748299717903, 0.012962467037141323, -0.011991272680461407, -0.007815799675881863, 0.04997354745864868, -0.012209296226501465, 0.0023999062832444906, -0.05718813091516495, -0.03136890381574631, 0.015948724001646042, -0.060517940670251846, 0.05993654578924179, 0.005757792852818966, 0.024048613384366035, -0.012288576923310757, 0.023189734667539597, -0.03224099799990654, -0.015340900979936123, -0.02686309441924095, 0.009302320890128613, -0.015446609817445278, 0.019397452473640442, 0.004951768089085817, -0.03649575263261795, 0.011277742683887482, -0.0013543862150982022, -0.029968272894620895, -0.04265325516462326, -0.0073731462471187115, 0.0501585379242897, 0.028039097785949707, 0.019265318289399147, -0.005156577564775944, 0.004016911145299673, -0.10940797626972198, 0.01790432445704937, 0.0677589476108551, -0.05169130489230156, -0.017151154577732086, 0.018419651314616203, 0.06363633275032043, 0.031871020793914795, 0.04291752725839615, 0.028514783829450607, -0.0015980105381458998, -0.06485197693109512, 0.023757915943861008, 0.004803115967661142, -0.02700844220817089, -0.018010033294558525, -0.0905919224023819, -0.02917546033859253, 0.004839452914893627, 0.07499995827674866, -0.021524829789996147, -0.008417014963924885, -0.034249454736709595, 0.027193432673811913, -0.0074788546189665794, 0.045375239104032516, -0.0010190929751843214, -0.001079379697330296, 0.03459300473332405, -0.06458770483732224, -0.03393232822418213, 0.013966694474220276, 0.02153804339468479, -0.018578214570879936, 0.025026414543390274, -0.017204007133841515, -0.06712470203638077, 0.05502111464738846, -0.07457713037729263, -0.030655374750494957, 0.027431275695562363, -0.015406969003379345, -0.009956390596926212, -0.012632128782570362, 0.00593287218362093, -0.04836149886250496, 0.007419393863528967, -0.003217492951080203, -0.0030589308589696884, 0.027563409879803658, -0.04146403819322586, 0.07558135688304901, -0.025475673377513885, -0.026387406513094902, -0.036892157047986984, -0.0018168595852330327, -0.03821351006627083, -0.03181816637516022, -0.03171245753765106, 0.0024775357451289892, 0.09233610332012177, -0.007009774446487427, 0.057928089052438736, 0.0031514253932982683, 0.019608870148658752, 0.0038352252449840307, 0.020269544795155525, 0.02682345360517502, -0.007961148396134377, -0.011826103553175926, 0.0007151819881983101, 0.009566591121256351, -0.007908293977379799, -0.01542018260806799, -0.0007667972822673619, -0.0011214978294447064, -0.057769525796175, 0.03274311125278473, 0.018697137013077736, -0.06242068484425545, 0.009844074957072735, -0.014680225402116776, 0.05428115651011467, -0.008489688858389854, 0.03892704099416733, 0.06902744621038437, -0.0625263974070549, 0.030443958938121796, -0.0786997452378273, -0.05103062838315964, -0.02170982025563717, -0.03205600753426552, 0.005754489451646805, 0.019027473405003548, -0.03937629982829094, -0.013471187092363834, -0.036363616585731506, -0.0033347629941999912, -0.015050203539431095, 0.001612875727005303, -0.017983606085181236, -0.002383389277383685, 0.006362311542034149, -0.03816065564751625, 0.027669118717312813, -0.01609407179057598, -0.012215903028845787, 0.010788842104375362, -0.0038847760297358036, 0.04550737515091896, -0.015684451907873154, 0.020097769796848297, -0.009540163911879063, -0.03208243474364281, 0.018446078523993492, -0.0034586398396641016, -0.027880534529685974, -0.008271666243672371, -0.0024758840445429087, 0.05100420117378235, 0.005278802942484617, 0.007260831538587809, 0.0016896793385967612, -0.025066055357456207, 0.012823725119233131, -0.044238876551389694, -0.02507926896214485, -0.01338529959321022, 0.0513477548956871, 0.06072935461997986, 0.00361720216460526, 0.016490478068590164, -0.00520612858235836, -0.009500524029135704, -0.01989956758916378, 0.05623675882816315, 0.0029912113677710295, 0.018419651314616203, 0.028752628713846207, 0.0024048613850027323, -0.03625790774822235, 0.01930495910346508, 0.019437093287706375, -0.041384756565093994, -0.008740746416151524, 0.01778540387749672, 0.017151154577732086, 0.04320822283625603, 0.007875259965658188, 0.0016764658503234386, 0.054386865347623825, 0.023189734667539597, -0.019886353984475136, 0.027404848486185074, -0.0266252513974905, 0.04511097073554993, 0.01847250573337078, -0.037579260766506195, 0.03274311125278473, -0.01668868027627468, -0.041569747030735016, -0.06649044901132584, 0.04859934002161026, 0.010326368734240532, -0.007412787061184645, -0.08646930009126663, -0.026545969769358635, 0.00672238040715456, -0.06464055925607681, 0.006349098403006792, -0.016067644581198692, -0.01113900076597929, -0.018221449106931686, 0.009877108968794346, -0.019912781193852425, -0.029492584988474846, 0.01930495910346508, -0.011905385181307793, 0.02772197313606739, 0.0030820544343441725, 0.07410144060850143, -0.005708242300897837, -0.012810511514544487, -0.008390587754547596, 0.023744702339172363, 0.011997879482805729, 0.003646932542324066, 0.009685512632131577, -0.07336148619651794, 0.026955587789416313, -0.01074920129030943, -0.015816587954759598, -0.02177588641643524, 0.06405916064977646, -0.03319237008690834, 0.04883718490600586, 0.024193963035941124, 0.010227267630398273, 0.0587209016084671, 0.043736763298511505, -0.027048083022236824, -0.033773768693208694, -0.0004571053432300687, -0.05171773210167885, -0.057980943471193314, -0.00438688974827528, -0.055813923478126526, 0.025713518261909485, -0.06855176389217377, 0.02774840034544468, 0.048942893743515015, 0.035438671708106995, 0.03773782402276993, -0.03549152612686157, -0.016886884346604347, 0.04030124843120575, -0.019701363518834114, -0.04032767564058304, 0.03345664218068123, -0.02453751303255558, 0.007419393863528967, -0.02004491537809372, 0.034223027527332306, 0.01338529959321022, -0.021881595253944397, 0.05214056372642517, 0.03623148053884506, -0.02626848593354225, 0.06622618436813354, -0.059408001601696014, -0.007135302759706974, 0.008879488334059715, -0.04289110004901886, -0.006735593546181917, 0.006487840320914984, 0.029492584988474846, 0.0037625508848577738, -0.01954280212521553, -0.08308663964271545, 0.04223042353987694, 0.09397458285093307, -0.04223042353987694, -0.05124204605817795, -0.03393232822418213, 0.01835358515381813, -0.02646668814122677, -0.036601461470127106, -0.012202689424157143, 0.008331126533448696, -0.04072408005595207, -0.03694501146674156, 0.05475684255361557, -0.0004760997835546732, -0.0044364407658576965, 0.01828751713037491, -0.010372616350650787, 0.039244167506694794, -0.0003177439502906054, -0.0276955459266901, -0.00899840984493494, 0.018842484802007675, -0.026123136281967163, -0.019556015729904175, -0.042071860283613205, -0.023599352687597275, -0.019080327823758125, 0.02011098340153694, -0.0276955459266901, 0.060782209038734436, -0.027021655812859535, -0.06416486948728561, 0.026929162442684174, 0.017772190272808075, -0.037817105650901794, -0.022238360717892647, -0.02156447060406208, 0.018432864919304848, 0.01832715794444084, -0.0031018746085464954, -0.02040168084204197, 0.04928644374012947, 0.0020167140755802393, -0.006368918344378471, 0.03940272703766823, 0.017151154577732086, -0.03871562331914902, -0.0658562034368515, -0.00041787768714129925, 0.016966164112091064, -0.012348038144409657, 0.027827681973576546, 0.016199780628085136, -0.03668074309825897, 0.0005933698266744614, -0.028303368017077446, -0.01292282622307539, 0.014389527030289173, -0.013021927326917648, -0.010465110652148724, -0.019397452473640442, -0.017137940973043442, -0.037341419607400894, 0.03744712471961975, -0.006705863401293755, -0.015235193073749542, 0.048678621649742126, 0.006517570465803146, 0.07114161550998688, -0.02263476699590683, 0.07452427595853806, 0.06548622250556946, -0.03107820823788643, 0.01249338686466217, -0.028091952204704285, -0.012942646630108356, -0.02727271243929863, -0.021432336419820786, -0.007141909562051296, 0.06543336808681488, 0.02049417607486248, 0.018274303525686264, -0.03033825010061264, 0.0024610187392681837, 0.039455581456422806, 0.003445426234975457, -0.0025006593205034733, -0.015235193073749542, -0.018551787361502647, -0.005318443290889263, -0.04014268517494202, 0.011020079255104065, 0.036152202636003494, -0.004129226319491863, -0.0019308262271806598, 0.021987304091453552, 0.022581912577152252, -0.0005685944342985749, 0.026308126747608185, 0.08424942940473557, 0.008469868451356888, 0.0501585379242897, -0.009639265947043896, 0.055602509528398514, -0.07764266431331635, -0.07283294200897217, -0.0012272059684619308, 0.04352534934878349, 0.014772719703614712, 0.07875259965658188, -0.007056021597236395, 0.005021139048039913, -0.0022562092635780573, 0.05993654578924179, 0.0272198598831892, -0.02962472103536129, -0.03726213797926903, 0.030761083588004112, -0.05877375230193138, 0.004832846112549305, 0.07827691733837128, -0.005054173059761524, -0.02408825419843197, -0.03221457079052925, 0.026876308023929596, 0.010868123732507229, -0.025554955005645752, 0.04762154072523117, 0.03631076216697693, 0.03866276890039444, 0.0008803509990684688, 0.02120770514011383, -0.04947143420577049, -0.006084827706217766, -0.007307078689336777, -0.06701899319887161, 0.030496813356876373, -0.02617599070072174, 0.008146136999130249, -0.021908022463321686, -0.02149840258061886, -0.07743124663829803, 0.05650102719664574, -0.04595663771033287, -0.0037361239083111286, -0.01921246387064457, -0.061997853219509125, -0.08398515731096268, 0.015274833887815475, -0.002138939220458269, 0.057452403008937836, -0.0265063289552927, -0.04201900586485863, 0.009513736702501774, 0.053224075585603714, -0.00071476906305179, 0.04125262051820755, -0.03464585915207863, -0.0037096969317644835, 0.01716436818242073, -0.04363105446100235, -0.008839847519993782, 0.03845135495066643, -0.02774840034544468, 0.05055494233965874, 0.03136890381574631, 0.012704803608357906, 0.005863501224666834, 0.003083706134930253, -0.0620507076382637, 0.01588265597820282, -0.0017458368092775345, -0.01728328876197338, 0.005992332939058542, 0.033060237765312195, -0.02751055732369423, 0.0018284213729202747, -0.04341964051127434, 0.04199257865548134, -0.014746292494237423, 0.023533286526799202, 0.052008431404829025, -0.010590638965368271, 0.02022990584373474, -0.0022248271852731705, -0.030206115916371346, -0.017706122249364853, -0.022449776530265808, 0.06675472110509872, 0.0858350545167923, -0.021789100021123886, -0.03646932542324066, 0.04976212978363037, 0.028752628713846207, 0.04178116098046303, -0.002996166469529271, 0.027536984533071518, 0.03528010845184326, -0.05750525742769241, -0.018657496199011803, -0.038794904947280884, 0.016609398648142815, 0.007663843687623739, -0.03202958032488823, 0.007214583922177553, 0.021009502932429314, 0.03932344540953636, 0.0027550198137760162, 0.019199250265955925, -0.03081393800675869, -0.01493128202855587, -0.004383586347103119, -0.036865729838609695, 0.039984121918678284, 0.010181020013988018, -0.025145335122942924, -0.027431275695562363, -0.007069235201925039, -0.060570795089006424, 0.039931267499923706, 0.022238360717892647, 0.001572409295476973, -0.024286456406116486, -0.023903263732790947, 0.04838792607188225, -0.005675208289176226, -0.01793075166642666, -0.009632659144699574, -0.021168064326047897, 0.02477535791695118, 0.011224888265132904, 0.011059719137847424, -0.007016381248831749, -0.06474626809358597, 0.012539634481072426, -0.007577955722808838, 0.02334829606115818, -0.005430758465081453, 0.03562365844845772, 0.0037592474836856127, 0.05517967417836189, 0.04482027143239975, 0.016543332487344742, 0.04191329702734947, -0.0022743777371942997, -0.00916357897222042, -0.011442911811172962, 0.01424417831003666, 0.06035937741398811, -0.027351994067430496, -0.04244183748960495, 0.025713518261909485, -0.012182869017124176, 0.022357283160090446, 0.07024309039115906, 0.022436562925577164, -0.029941845685243607, 0.027378421276807785, -0.02560780942440033, 0.018670709803700447, 0.0076704504899680614, 0.017256861552596092, 0.012440532445907593, 0.015235193073749542, 0.012678376398980618, 0.07991538941860199, -0.02745770290493965, 0.010161199606955051, -0.013702424243092537, 0.009639265947043896, -0.0037856746930629015, -0.016900096088647842, 0.03300738334655762, -0.00916357897222042, 0.007558135781437159, 0.0046610706485807896, -0.026400620117783546, -0.004595003090798855, -0.013431547209620476, 0.02132662758231163, -0.0265063289552927, 0.00022586867271456867, -0.007987575605511665, -0.033298078924417496, 0.03773782402276993, -0.024008972570300102, 0.05708242207765579, 0.009744973853230476, 0.028382649645209312, -0.015406969003379345, -0.03665431588888168, -0.00016640781541354954, -0.00471392460167408, -0.06004225090146065, -0.02096986211836338, -0.02891119010746479, -0.017719335854053497, -0.01754755899310112, -0.031871020793914795, -0.04244183748960495, -0.006167412269860506, -0.050105683505535126, 0.014230964705348015, -0.002337142126634717, 0.01888212561607361, 0.00813292432576418, -0.0008613565587438643, 0.05951371043920517, -0.01704544574022293, -0.027325566858053207, -0.03559723496437073, -0.002214916981756687, -0.0028640313539654016, 0.02061309665441513, 0.003775764489546418, -0.006236783228814602, -0.003121695015579462, 0.016530118882656097, -0.004512418527156115, 0.09450311958789825, -0.02988899126648903, 0.004010304342955351, 0.031448185443878174, -0.0009546771179884672, -0.023876838386058807, -0.03229385241866112, 0.044688139110803604, 0.022410135716199875, -0.04267968237400055, -0.02260833978652954, 0.009203219786286354, -0.04001054912805557, 0.013821345753967762, -0.015935510396957397, -0.004512418527156115, -0.02677059918642044, -0.00807346310466528, -0.017230434343218803, -0.008000788278877735, 0.030946072190999985, -0.05412259325385094, 0.025264257565140724, 0.046115197241306305, 0.020917007699608803, 0.010874730534851551, 0.015618384815752506, 0.007901687175035477, 0.0015624992083758116, -0.00972515344619751, -0.022819755598902702, -0.022568698972463608, 0.023691847920417786, 0.0016037914901971817, -0.02795981615781784, -0.010220660828053951, -0.001275105052627623, -0.004185383673757315, 0.0006528306403197348, -0.0023090632166713476, -0.009599625132977962, 0.008813420310616493, 0.01906711421906948, -0.027801254764199257, 0.03559723496437073, 0.01137684378772974, 0.04352534934878349, -0.005922961980104446, -0.010498144663870335, -0.03694501146674156, 0.025211403146386147, 0.024696076288819313, -0.019318172708153725, -0.04637946933507919, 0.006890852469950914, -0.0035775615833699703, -0.012486780062317848, -0.004974891897290945, 0.02028275839984417, -0.048229362815618515, 0.010240481235086918, 0.013358872383832932, 0.024352524429559708, -0.011561833322048187, -0.0006313587073236704, -0.07029594480991364, 0.039482008665800095, 0.022383708506822586, -0.022595126181840897, -0.011964845471084118, -0.011178641580045223, 0.021260559558868408, -0.04360462725162506, -0.06337206065654755, -0.027563409879803658, -0.003141515189781785, 0.0004773385589942336, 0.010075312107801437, -0.03152746707201004, 0.04593021050095558, 0.0071815503761172295, -0.0005491870688274503, 0.025858866050839424, -0.0005607489147223532, 0.008542543277144432, -0.03845135495066643, 0.03718285635113716, 0.014614157378673553, 0.03868919610977173, -0.018895339220762253, -0.010630279779434204, -0.0038286184426397085, -0.011826103553175926, -0.005275499541312456, -0.0012907960917800665, -0.03131605312228203, -0.023638993501663208, 0.002756671514362097, -0.014548089355230331, 0.018076101318001747, 0.011660934425890446, -0.004670980852097273, 0.004651160445064306, 0.022436562925577164, 0.015869442373514175, -0.010590638965368271, -0.023929690942168236, -0.051770586520433426, -0.0016459095058962703, -0.004429833963513374, -0.06527480483055115, -0.013953480869531631, -0.04558665677905083, -0.04336678609251976, 0.020031701773405075, 0.031897448003292084, -0.040169112384319305, 0.03940272703766823, 0.0033628419041633606, -0.006501053925603628, 0.012506600469350815, 0.007663843687623739, 0.021762674674391747, 0.044952407479286194, 0.029334023594856262, 0.009645872749388218, 0.03057609498500824, 0.010346189141273499, -0.0065968516282737255, 0.016701893880963326, 0.014627370983362198, 0.017534345388412476, 0.014455595053732395, -0.009639265947043896, -0.001313093933276832, 0.013887413777410984, 0.016173353418707848, -0.034275881946086884, 0.02596457488834858, 0.048017945140600204, 0.028276940807700157, -0.04725155979394913, -0.013438154011964798, -0.015816587954759598, 0.043234650045633316, 0.04384247213602066, 0.0004310912045184523, -0.02170982025563717, 0.034487295895814896, 0.03985198959708214, -0.040406957268714905, -0.02418074943125248, 0.006187232676893473, -0.00872753281146288, -0.006088131107389927, -0.02007134258747101, -0.014865214005112648, 0.021009502932429314, -0.002821087371557951, -0.060782209038734436, 0.032610975205898285, 0.03964057192206383, -0.008945555426180363, 0.01638476923108101, 0.013530648313462734, -0.013940267264842987, 0.013372085988521576, -0.07563421130180359, -0.026374192908406258, -0.007895080372691154, 0.01573730632662773, -0.02156447060406208, -0.019344598054885864, -0.015829801559448242, 0.030047552660107613, 0.030443958938121796, 0.03195030242204666, 0.04833507165312767, -0.0891648605465889, -0.0029053236357867718, 0.005615747533738613, -0.008879488334059715, 0.031104635447263718, 0.04294395074248314, -0.010491537861526012, -0.040169112384319305, -0.04598306119441986, -0.024590367451310158, -0.049392152577638626, 0.019648509100079536, 0.06390060484409332, 7.091945735737681e-05, -0.014178111217916012, 0.019529588520526886, 0.02626848593354225, -0.006022063549607992, 0.02266119420528412, 0.01823466271162033, -0.017507918179035187, -0.02201373130083084, 0.022502630949020386, 0.025858866050839424, 0.0013230040203779936, 0.021577684208750725, 0.005341567099094391, 0.05903802439570427, -0.015843015164136887, -0.047040145844221115, -0.03253169730305672, 0.009084297344088554, -0.06257925182580948, -0.026043854653835297, -0.05475684255361557, 0.0007866175728850067, -0.021762674674391747, 0.021762674674391747, 0.020626310259103775, 0.015724092721939087, -0.03773782402276993, -0.01275765709578991, -0.04458243027329445, -0.005543073173612356, -0.009209825657308102, -0.0007048589177429676, -0.025647450238466263, -0.04172830656170845, 0.01143630500882864, 0.04223042353987694, 0.02456394024193287, 0.006676132790744305, 0.000691232446115464, 0.03488370403647423, -0.031183917075395584, 0.01992599479854107, 0.024233601987361908, 0.01213662140071392, 0.005833770614117384, -0.017534345388412476, 0.04381604492664337, 0.013471187092363834, 0.01384777296334505, 0.03602006658911705, -8.841705857776105e-05, -0.043763190507888794, 0.0032604369334876537, 0.05079278722405434, -0.028594065457582474, 0.054175447672605515, 0.01590908318758011, 0.008060249499976635, -0.032637402415275574, 0.0011570091592147946, 0.04003697633743286, -0.02099628932774067, -0.014270605519413948, 0.05480969697237015, -0.028303368017077446, 0.03292810171842575, 0.010689741000533104, -0.009513736702501774, 0.028065524995326996, -0.031844593584537506, 0.05422830209136009, 0.030708229169249535, 0.03797566890716553, -0.02655918337404728, 0.020480962470173836, -0.02917546033859253, -0.006078220903873444, -0.02123413234949112, 0.01054439228028059, -0.055813923478126526, 0.0036634495481848717, 0.02189480885863304, -0.027933388948440552, 0.05428115651011467, -0.010993652045726776, -0.01695295050740242, -0.018419651314616203, 0.024167535826563835, -0.012096981517970562, -0.010313155129551888, 0.020150624215602875, -0.023903263732790947, -0.003927719779312611, 0.01387420017272234, 0.023335082456469536, -0.02382398396730423, -0.03269025683403015, -0.017653267830610275, 0.028356222435832024, -0.031871020793914795, -0.04532238841056824, 0.03607292100787163, -0.008337733335793018, -0.000635900825727731, -0.02085094153881073, 0.005007925443351269, 0.012301790527999401, -0.006157502066344023, 0.019080327823758125, 0.045613083988428116, 0.0076704504899680614, 0.04796509072184563, -0.002024972578510642, -0.018776416778564453, 0.06485197693109512, -0.002322276821359992, -0.00883324071764946, -0.01579016074538231, 0.014138470403850079, -0.02349364571273327, -0.021908022463321686, -0.03221457079052925, 0.05097777396440506, 0.008991803042590618, 0.012513207271695137, 0.02037525363266468, -0.011991272680461407, 0.018578214570879936, 0.037130001932382584, -0.046828728169202805, -0.0068512121215462685, 0.012149835005402565, -0.02278011478483677, 0.03081393800675869, 0.020203478634357452, 0.014283819124102592, 0.01802324689924717, 0.04809722676873207, -0.00831130612641573, -0.013927053660154343, -0.02751055732369423, -0.001368425553664565, 0.012400892563164234, -0.010669920593500137, 0.012301790527999401, 0.010161199606955051, 0.04035410284996033, 0.017891110852360725, -0.009778007864952087, 0.025858866050839424, -0.01045189704746008, 0.04080336168408394, 0.01061706617474556, -0.030417531728744507, 0.018538573756814003, -0.0058502876199781895, 0.03715642914175987, -0.019833499565720558, 0.037552833557128906, 0.01576373353600502, -0.005569500382989645, 0.03633718937635422, -0.014415954239666462, -0.00012139925092924386, -0.007115482352674007, -0.00295157078653574, -0.008509509265422821, 0.009322141297161579, 0.029730428010225296, -0.04603591561317444, -0.060570795089006424, 0.01506341714411974, -0.02567387744784355, 0.006008849944919348, 0.01987314037978649, -0.04352534934878349, 0.04368390887975693, 0.0026096708606928587, 0.004832846112549305, -0.028752628713846207, 0.04312894120812416, -0.03419660031795502, -0.01859142817556858, -0.03620505705475807, 0.033324506133794785, 0.0265063289552927, 0.02213265188038349, 0.04511097073554993, -0.02156447060406208, -0.004109405912458897, 0.01749470643699169, -0.008694498799741268, 0.0008514464134350419, 0.0009406377212144434, -0.001663252362050116, 0.018300730735063553, 0.0071815503761172295, 0.02670453116297722, -0.04767439514398575, -0.03974628075957298, -0.011911991983652115, 0.02367863431572914]
        return temp_embedding