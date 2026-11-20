import json
from .database import SessionLocal, Base, engine
from .models import Package

PACKAGES_SEED = [
    {
        "slug": "coorg-chikmagalur",
        "name": "Coorg & Chikmagalur Coffee Hills",
        "tagline": "Golden temples, misty peaks, thundering waterfalls & elephants by the river — the Scotland of India",
        "duration": "3 Days · 2 Nights",
        "price": 6999,
        "original_price": 7999,
        "advance_price": 2100,
        "emoji": "☕",
        "badge": "Bestseller",
        "category": "Hill Station",
        "colors": json.dumps({"primary": "#0b8a8f", "accent": "#ff7a1a"}),
        "active": True,
        "is_sample": True,
        "description": "Escape the city rush and immerse yourself in the emerald coffee plantations of Karnataka. From the serene chants of Bylakuppe Tibetan Monastery to conquering the highest peak in Karnataka (Mullayanagiri), cascading Abbey Falls, and peaceful elephant encounters at Dubare, this is an unforgettable nature retreat.",
        "highlights": json.dumps([
            "9 Iconic spots covered across Coorg & Chikmagalur",
            "2 Misty mountain summits: Mullayanagiri & Baba Budangiri",
            "2 Roaring waterfalls: Abbey Falls & Hebbe Falls",
            "Bylakuppe Namdroling Monastery (Golden Temple)",
            "Dubare Elephant Camp by the Cauvery river",
            "Private coffee estate nature walk and tasting"
        ]),
        "itinerary": json.dumps([
            {
                "day": 1,
                "title": "Hyderabad Departure & Coorg Arrival",
                "desc": "Board the overnight train/bus from Hyderabad. Arrive in Mysore/Bangalore in the morning and transfer to our private vehicle. Head towards Coorg with a breakfast stop at Maddur. Visit the majestic Namdroling Monastery (Golden Temple) in Bylakuppe. Check in to our cozy stay, visit Raja's Seat for a magical sunset, and enjoy a group bonfire dinner.",
                "meals": "Dinner included",
                "stay": "Resort / Homestay in Coorg"
            },
            {
                "day": 2,
                "title": "Chikmagalur Peaks & Coffee Country",
                "desc": "Wake up to fresh mountain mist. Journey towards the rolling Western Ghats of Chikmagalur. Trek up to Mullayanagiri peak (highest point in Karnataka) and take in 360-degree views above the clouds. Explore Baba Budangiri caves and Z-Point viewpoint. Walk through lush aromatic coffee estates. Evening group fun and music under the stars.",
                "meals": "Breakfast & Dinner",
                "stay": "Scenic Estate Stay in Chikmagalur"
            },
            {
                "day": 3,
                "title": "Waterfalls, Elephants & Return Journey",
                "desc": "Morning visit to Abbey Falls surrounded by spice trees. Head to Dubare Elephant Camp for river rafting and elephant interactions. Stop for authentic Coorg homemade chocolates, spices and coffee shopping. Board return train/bus to Hyderabad with unforgettable memories.",
                "meals": "Breakfast",
                "stay": "Overnight journey"
            }
        ]),
        "inclusions": json.dumps([
            "Hyderabad to Karnataka return Sleeper class train tickets",
            "All 3 days private Tempo Traveller transport with courteous driver",
            "2 Nights comfortable accommodation (sharing basis)",
            "Experienced HappyMiles Trip Captain throughout the journey",
            "All toll taxes, state permits, parking fees & driver allowances",
            "First Aid kit and 24/7 organizer assistance"
        ]),
        "exclusions": json.dumps([
            "Food and daily meals not specifically listed",
            "Jeep safari / off-road ride fees at special viewpoints",
            "Entry tickets to monuments and adventure activities",
            "Personal expenses, shopping & tips"
        ]),
        "pickup_points": "Uppal, LB Nagar, Lakdikapul, Kukatpally, Gachibowli (Hyderabad)",
        "best_season": "September to May (Pleasant weather & coffee blooms)",
        "cancellation_policy": "Full refund if cancelled 7 days prior to departure. 50% refund 3-6 days prior. No refund within 48 hours.",
        "image_card": "/static/images/places/coorg-chikmagalur/coorg-chikmagalur-poster-900w.webp",
        "image_hero": "/static/images/places/coorg-chikmagalur/coorg-mountain-ridge.webp",
        "gallery_images": json.dumps([
            "/static/images/places/coorg-chikmagalur/coorg-chikmagalur-poster.webp",
            "/static/images/places/coorg-chikmagalur/coorg-mountain-ridge.webp",
            "/static/images/happy-customers/coorg-bylakuppe-monastery.webp",
            "/static/images/happy-customers/chikmagalur-coffee-trail-trek.webp",
            "/static/images/happy-customers/coorg-viewpoint-rockfall.webp",
            "/static/images/happy-customers/maddur-highway-journey-stop.webp"
        ])
    },
    {
        "slug": "araku-vanjangi-lambasingi",
        "name": "Araku Valley, Vanjangi & Lambasingi + Vizag",
        "tagline": "Witness the ethereal sea of clouds sunrise, explore million-year-old caves & chill at the Kashmir of Andhra",
        "duration": "4 Days · 3 Nights",
        "price": 6999,
        "original_price": 7999,
        "advance_price": 2100,
        "emoji": "☁️",
        "badge": "Every Thursday Departure",
        "category": "Hill Station & Coastal",
        "colors": json.dumps({"primary": "#1f7a8c", "accent": "#ff8c42"}),
        "active": True,
        "is_sample": True,
        "description": "The ultimate budget escape from Hyderabad! Stand above a sweeping ocean of clouds at the Vanjangi Hills sunrise, experience near-freezing winter mists in Lambasingi, marvel at Borra Caves stalactites, and wind down along RK Beach Vizag with a lively beach campfire.",
        "highlights": json.dumps([
            "Vanjangi Sea of Clouds 5:00 AM Sunrise Trek",
            "Lambasingi - the Kashmir of Andhra Pradesh with cold pine mist",
            "Million-year-old limestone Borra Caves",
            "Paderu coffee estates & Katiki Waterfalls",
            "Visakhapatnam RK Beach & Submarine Museum",
            "Bonfire, music and stargazing tent camping"
        ]),
        "itinerary": json.dumps([
            {
                "day": 1,
                "title": "Departure from Hyderabad",
                "desc": "Meet your HappyMiles trip captain at Uppal / Secunderabad station. Board the evening train towards Visakhapatnam. Bond with fellow travelers over games and travel stories.",
                "meals": "Snacks",
                "stay": "Overnight train"
            },
            {
                "day": 2,
                "title": "Araku Valley, Borra Caves & Lambasingi",
                "desc": "Arrive at Vizag early morning, board our private Tempo Traveller. Drive up the scenic Eastern Ghats ghat road to Borra Caves. Savor famous Araku bamboo chicken and hot ginger tea at the Coffee Museum. Transfer to Lambasingi, set up camp, light the bonfire, and enjoy barbecue under starry skies.",
                "meals": "Dinner & BBQ",
                "stay": "Camp / Tent in Lambasingi"
            },
            {
                "day": 3,
                "title": "Vanjangi Sea of Clouds Sunrise & Vizag Beach",
                "desc": "Early morning 4:30 AM drive to Vanjangi hill base. Short hike to the peak to witness the breathtaking sunrise over a rolling blanket of clouds. Head down for a hearty South Indian breakfast. Drive down to Visakhapatnam, visit RK Beach, INS Kursura Submarine Museum, and catch the sunset at Kailasagiri hill.",
                "meals": "Breakfast",
                "stay": "Hotel in Vizag"
            },
            {
                "day": 4,
                "title": "Vizag Sightseeing & Return to Hyderabad",
                "desc": "Morning beach walk at Rushikonda Beach, optional water sports. Visit Ross Hill and local cashew markets. Board the evening return train to Hyderabad, reaching next morning at 6:30 AM.",
                "meals": "Breakfast",
                "stay": "Overnight train"
            }
        ]),
        "inclusions": json.dumps([
            "Hyderabad <-> Vizag Sleeper class train tickets",
            "Private Tempo Traveller transport for all internal transfers",
            "Budget sharing stays: Paderu, Lambasingi (tent) & Vizag hotel",
            "Trip organizer & bonfire experience",
            "Tolls, parking permits, driver charges included"
        ]),
        "exclusions": json.dumps([
            "Daily food & meals not specified",
            "Borra caves, museum and viewpoint entry tickets",
            "Zipline & optional water sports",
            "Personal expenses"
        ]),
        "pickup_points": "Uppal, Secunderabad Station, Kacheguda (Hyderabad)",
        "best_season": "October to March (Peak cloud formation)",
        "cancellation_policy": "Full refund if cancelled 7 days prior. 50% refund 3-6 days prior. No refund within 48 hours.",
        "image_card": "/static/images/places/araku-vanjangi-lambasingi/araku-vanjangi-poster-900w.webp",
        "image_hero": "/static/images/places/araku-vanjangi-lambasingi/araku-tea-gardens.webp",
        "gallery_images": json.dumps([
            "/static/images/places/araku-vanjangi-lambasingi/araku-vanjangi-poster.webp",
            "/static/images/places/araku-vanjangi-lambasingi/araku-tea-gardens.webp"
        ])
    },
    {
        "slug": "gokarna-dandeli-murudeshwar",
        "name": "Gokarna, Dandeli & Murudeshwar",
        "tagline": "Whitewater rafting by day, campfires by night, ancient sea forts and giant Shiva deity on the Arabian Sea",
        "duration": "3 Days · 2 Nights",
        "price": 5499,
        "original_price": 6000,
        "advance_price": 1650,
        "emoji": "🌊",
        "badge": "Adventure Special",
        "category": "Beach & Adventure",
        "colors": json.dumps({"primary": "#028090", "accent": "#f0a500"}),
        "active": True,
        "is_sample": True,
        "description": "The ultimate adrenaline and chill combo! Conquer Grade-3 whitewater rapids on the Kali River in Dandeli, swim in crystal clear Vibhuti waterfalls, cruise through Honnavar mangroves, stand in awe before the towering 123-foot Murudeshwar Shiva idol, and relax at Om Beach in Gokarna.",
        "highlights": json.dumps([
            "Dandeli Whitewater River Rafting & Kali River adventures",
            "Majestic 123-foot Lord Shiva statue overlooking the Arabian sea",
            "Vibhuti Waterfalls natural jungle pool swim",
            "Sharavathi river backwaters boat cruise in Honnavar",
            "Sunset at Om Beach & Kudle Beach in Gokarna",
            "16th-century Mirjan Fort architectural exploration"
        ]),
        "itinerary": json.dumps([
            {
                "day": 1,
                "title": "Dandeli River Adventure & Jungle Stay",
                "desc": "Arrive in Hubli/Alnavar by morning train, transfer to Dandeli. Check into our riverside camp. Gear up for exhilarating whitewater rafting, kayaking, and natural jacuzzi baths on the Kali River. Evening campfire with music and delicious North Karnataka dinner.",
                "meals": "Lunch & Dinner included",
                "stay": "Riverside Adventure Camp in Dandeli"
            },
            {
                "day": 2,
                "title": "Vibhuti Waterfalls, Honnavar Mangroves & Murudeshwar",
                "desc": "Morning trek through dense forest to the pristine Vibhuti Falls. Dip in turquoise waters. Head towards Honnavar for an enchanting boat ride through mangrove tunnels. Drive along the coastal highway to Murudeshwar. Visit the colossal Shiva statue and Rajagopuram at sunset.",
                "meals": "Breakfast",
                "stay": "Coastal Hotel near Murudeshwar / Gokarna"
            },
            {
                "day": 3,
                "title": "Gokarna Beach Trek, Mirjan Fort & Departure",
                "desc": "Visit the sacred Mahabaleshwar Temple in Gokarna. Embark on the famous beach trek: Kudle Beach to Om Beach. Explore the moss-covered stone walls of Mirjan Fort. Relish fresh coastal seafood. Evening transfer to railway station for departure.",
                "meals": "Breakfast",
                "stay": "Overnight train"
            }
        ]),
        "inclusions": json.dumps([
            "Sleeper class train tickets from Hyderabad / Vijayawada / Bangalore",
            "Private transportation for all 3 days",
            "2 Nights accommodation (1 night Dandeli camp, 1 night coastal hotel)",
            "All meals in Dandeli included",
            "Basic water activities with safety gear & life jackets",
            "Trip captain assistance throughout",
            "Driver charges, tolls, parking and state taxes"
        ]),
        "exclusions": json.dumps([
            "Food outside Dandeli & entry tickets unless specified",
            "Long-run Grade 3+ extreme rafting addon",
            "Personal expenses & watersports at beach"
        ]),
        "pickup_points": "Secunderabad, Begumpet, Lingampalli (Hyderabad)",
        "best_season": "October to May (Ideal for water rafting & beach walks)",
        "cancellation_policy": "Full refund if cancelled 7 days prior. 50% refund 3-6 days prior. No refund within 48 hours.",
        "image_card": "/static/images/places/gokarna-dandeli-murudeshwar/gokarna-dandeli-poster-900w.webp",
        "image_hero": "/static/images/places/gokarna-dandeli-murudeshwar/murudeshwar-coastal-cliff.webp",
        "gallery_images": json.dumps([
            "/static/images/places/gokarna-dandeli-murudeshwar/gokarna-dandeli-poster.webp",
            "/static/images/places/gokarna-dandeli-murudeshwar/murudeshwar-coastal-cliff.webp"
        ])
    },
    {
        "slug": "kerala",
        "name": "Kerala — God's Own Country",
        "tagline": "Glide through tranquil Alleppey backwaters, wander rolling Munnar tea estates & spot wildlife in Thekkady",
        "duration": "5 Days · 4 Nights",
        "price": 14999,
        "original_price": 16999,
        "advance_price": 4500,
        "emoji": "🌴",
        "badge": "Signature Journey",
        "category": "Backwaters & Hill Station",
        "colors": json.dumps({"primary": "#1b4965", "accent": "#f39c12"}),
        "active": True,
        "is_sample": True,
        "description": "Experience the magic of Kerala with a balanced itinerary covering Munnar's rolling tea carpets, Thekkady's aromatic spice plantations & Periyar lake, and the serene palm-fringed backwaters of Alleppey. Includes comfortable resort stays, daily breakfast & dinner.",
        "highlights": json.dumps([
            "Alleppey Backwaters Traditional Houseboat / Shikara Cruise",
            "Munnar rolling tea plantations, Mattupetty Dam & Echo Point",
            "Thekkady Periyar Wildlife Sanctuary & Spice Garden Tour",
            "Cheeyappara & Valara cascading waterfalls",
            "Authentic Kerala Sadya lunch experience",
            "Kalaripayattu martial arts & Kathakali cultural show"
        ]),
        "itinerary": json.dumps([
            {
                "day": 1,
                "title": "Kochi Arrival & Journey to Munnar",
                "desc": "Arrive in Kochi, where our private AC vehicle greets you. Drive through lush Western Ghats, stopping at Cheeyappara and Valara waterfalls. Check in to your tea-garden resort in Munnar. Evening at leisure strolling through local spice markets.",
                "meals": "Dinner",
                "stay": "Hill Resort in Munnar"
            },
            {
                "day": 2,
                "title": "Munnar Tea Hills & Scenic Lakes",
                "desc": "Full day sightseeing in Munnar. Visit Eravikulam National Park (Nilgiri Tahr), Tea Museum with fresh brew tasting, Mattupetty Dam, Echo Point, and Kundala Lake. Watch the sunset painting the hills gold.",
                "meals": "Breakfast & Dinner",
                "stay": "Hill Resort in Munnar"
            },
            {
                "day": 3,
                "title": "Munnar to Thekkady Spice Sanctuary",
                "desc": "Scenic drive to Thekkady. Check in to your hotel and visit an organic spice plantation to see cardamom, cinnamon and pepper growing. Enjoy a scenic boat ride in Periyar Lake spotting wild elephants and bison. Attend a traditional Kalaripayattu martial arts show.",
                "meals": "Breakfast & Dinner",
                "stay": "Hotel in Thekkady"
            },
            {
                "day": 4,
                "title": "Thekkady to Alleppey Houseboat Backwaters",
                "desc": "Head towards Alleppey, the Venice of the East. Board your traditional Kerala houseboat/cruise. Drift along palm-shaded canals, watching tranquil village life, paddy fields and lotus blooms. Savor freshly prepared Kerala cuisine on board.",
                "meals": "Breakfast, Lunch & Dinner",
                "stay": "Resort / Premium Houseboat in Alleppey"
            },
            {
                "day": 5,
                "title": "Kochi Sightseeing & Farewell",
                "desc": "After breakfast, drive to Fort Kochi. Stroll by Chinese Fishing Nets, St. Francis Church, and colorful Jew Town. Transfer to Kochi Airport / Railway station with cherished memories.",
                "meals": "Breakfast",
                "stay": "Return journey"
            }
        ]),
        "inclusions": json.dumps([
            "4 Nights comfortable accommodation (2N Munnar, 1N Thekkady, 1N Alleppey)",
            "Daily delicious Breakfast and Dinner at all hotels",
            "Private AC transport for all transfers and sightseeing",
            "Alleppey backwaters boat cruise experience",
            "Dedicated HappyMiles trip coordinator support",
            "All toll, parking, driver allowances and taxes"
        ]),
        "exclusions": json.dumps([
            "Train/flight tickets from Hyderabad (can be booked on request)",
            "Lunches (except on full-day houseboat)",
            "Entry fees for national parks, boat safaris & cultural shows",
            "Personal activities & Ayurvedic spa treatments"
        ]),
        "pickup_points": "Pickup from Kochi Airport/Ernakulam Station (Hyderabad flight/train coordination included)",
        "best_season": "September to April (Lush greenery and cool climate)",
        "cancellation_policy": "Full refund 10 days prior. 50% refund 4-9 days prior. No refund within 72 hours.",
        "image_card": "/static/images/places/kerala/kerala-poster-900w.webp",
        "image_hero": "/static/images/places/kerala/alleppey-houseboat.webp",
        "gallery_images": json.dumps([
            "/static/images/places/kerala/kerala-poster.webp",
            "/static/images/places/kerala/alleppey-houseboat.webp",
            "/static/images/places/kerala/munnar-tea-hills.webp",
            "/static/images/places/kerala/thekkady-wildlife.webp"
        ])
    },
    {
        "slug": "ooty-coonoor",
        "name": "Ooty & Coonoor Backpacking Trip",
        "tagline": "Queen of Nilgiri Hills, pine forests, Dolphin's Nose viewpoint and 100% Free Heritage Toy Train ride",
        "duration": "3 Days · 2 Nights",
        "price": 7499,
        "original_price": 8499,
        "advance_price": 1500,
        "emoji": "🚂",
        "badge": "Free Toy Train Ride",
        "category": "Hill Station & Heritage",
        "colors": json.dumps({"primary": "#2d6a4f", "accent": "#e76f51"}),
        "active": True,
        "is_sample": True,
        "description": "Board the world-famous UNESCO Heritage Nilgiri Mountain Toy Train for FREE on this enchanting backpacking journey! Travel through Bandipur forest, breathe crisp pine forest air, admire panoramic views from Dolphin's Nose in Coonoor, and taste fresh handmade Nilgiri chocolates.",
        "highlights": json.dumps([
            "100% FREE Nilgiri Mountain Toy Train Ride experience",
            "Bandipur Tiger Reserve scenic forest drive",
            "Dolphin's Nose & Catherine Falls viewpoint in Coonoor",
            "Pykara Lake boating & cascading Pykara Waterfalls",
            "Tea Factory walk and chocolate tasting session",
            "Needle Rock Viewpoint & Pine Forest walk"
        ]),
        "itinerary": json.dumps([
            {
                "day": 1,
                "title": "Bandipur Forest Drive & Ooty Arrival",
                "desc": "Overnight journey from Hyderabad. Morning drive through the dense Bandipur Tiger Reserve safari route, spotting deers and wild peacocks. Climb the 36 hairpin bends of Nilgiris to Ooty. Visit the picturesque Pine Forest and Pykara waterfalls. Check in to our hotel and enjoy an evening group dinner.",
                "meals": "Dinner",
                "stay": "Hotel in Ooty"
            },
            {
                "day": 2,
                "title": "Heritage Toy Train Ride & Coonoor Vistas",
                "desc": "Morning boarding of the iconic UNESCO Nilgiri Toy Train to Coonoor through misty tunnels and tea valleys. Visit Dolphin's Nose viewpoint offering panoramic vistas of Catherine Falls. Tour an authentic Nilgiri Tea Factory, sample exotic tea blends, and explore Sim's Park botanical gardens.",
                "meals": "Breakfast & Dinner",
                "stay": "Hotel in Ooty"
            },
            {
                "day": 3,
                "title": "Botanical Gardens, Mysore Palace & Return",
                "desc": "Visit Ooty Government Botanical Garden and local homemade chocolate stores. Drive down to Mysore, stop to admire the magnificent illuminated Mysore Palace. Board the evening train back to Hyderabad.",
                "meals": "Breakfast",
                "stay": "Overnight journey"
            }
        ]),
        "inclusions": json.dumps([
            "Hyderabad <-> Bangalore/Mysore sleeper train tickets",
            "Private vehicle for all 3 days in Nilgiris",
            "2 Nights hotel accommodation in Ooty",
            "Confirmed Nilgiri Mountain Toy Train ticket (100% Free)",
            "Trip captain and first aid support",
            "All toll, parking, driver charges and state road permits"
        ]),
        "exclusions": json.dumps([
            "Meals not specified in the itinerary",
            "Entry tickets to botanical gardens & Mysore palace",
            "Pykara boat ride charges",
            "Personal shopping & woolen purchases"
        ]),
        "pickup_points": "Uppal, LB Nagar, Lakdikapul, Shamshabad (Hyderabad)",
        "best_season": "All Year Round (Summer escape in Apr-Jun, Winter mist in Oct-Feb)",
        "cancellation_policy": "Full refund if cancelled 7 days prior. 50% refund 3-6 days prior. No refund within 48 hours.",
        "image_card": "/static/images/places/ooty-coonoor/ooty-coonoor-poster-900w.webp",
        "image_hero": "/static/images/places/ooty-coonoor/ooty-pine-hills.webp",
        "gallery_images": json.dumps([
            "/static/images/places/ooty-coonoor/ooty-coonoor-poster.webp",
            "/static/images/places/ooty-coonoor/ooty-pine-hills.webp"
        ])
    },
    {
        "slug": "shimla-manali",
        "name": "Himachal: Shimla & Manali with Kasol & Manikaran",
        "tagline": "Snow-capped Himalayan peaks, pine-scented valleys, Parvati river trails & sacred hot springs",
        "duration": "6 Days · 5 Nights",
        "price": 10999,
        "original_price": 13999,
        "advance_price": 3300,
        "emoji": "🏔️",
        "badge": "Himalayan Expedition",
        "category": "Snow & Adventure",
        "colors": json.dumps({"primary": "#1d3557", "accent": "#e63946"}),
        "active": True,
        "is_sample": True,
        "description": "The ultimate North India getaway! Walk the historic British Ridge & Mall Road in Shimla, witness snow-clad peaks and paraglide in Solang Valley Manali, experience the bohemian vibes of Kasol along the Parvati River, and take a holy dip in the natural hot springs of Manikaran Sahib.",
        "highlights": json.dumps([
            "Shimla Mall Road, Christ Church & The Ridge walking tour",
            "Solang Valley snow adventures & Atal Tunnel gateway",
            "Kasol - the hippie wonderland in Parvati Valley",
            "Manikaran Sahib Gurudwara & therapeutic natural hot springs",
            "Ancient Hadimba Devi wooden temple in Manali deodar forest",
            "Jogini Waterfall nature trek & Old Manali cafe hopping"
        ]),
        "itinerary": json.dumps([
            {
                "day": 1,
                "title": "Delhi Meetup & Overnight Drive to Shimla",
                "desc": "Meet your trip captain in Delhi (Majnu Ka Tila / Kashmiri Gate) by 8:00 PM. Board luxury AC Volvo bus. Overnight journey through the foothills of the Himalayas.",
                "meals": "Water bottle provided",
                "stay": "Overnight Volvo bus"
            },
            {
                "day": 2,
                "title": "Shimla Colonial Charm & Kufri",
                "desc": "Arrive in Shimla in the morning, check in to hotel. Head to Kufri for breathtaking valley views and horse riding. In the afternoon, take a leisurely stroll across Mall Road, visit the iconic Christ Church, Lakkar Bazaar, and The Ridge. Group dinner at hotel.",
                "meals": "Breakfast & Dinner",
                "stay": "Hotel in Shimla"
            },
            {
                "day": 3,
                "title": "Shimla to Manali via Kullu Valley",
                "desc": "Check out and drive towards Manali along the gushing Beas River. Stop at Pandoh Dam and Hanogi Mata Temple. Visit Kullu Shawl weaving factory and enjoy optional river rafting on the Beas River. Check in to your hotel in Manali.",
                "meals": "Breakfast & Dinner",
                "stay": "Hotel in Manali"
            },
            {
                "day": 4,
                "title": "Solang Valley Snow Point & Old Manali",
                "desc": "Full day dedicated to Solang Valley. Enjoy snow activities, skiing, zorbing, and paragliding with majestic snow peaks as backdrop. Visit Hadimba Temple, Vashisht hot springs, and chill at funky cafes in Old Manali.",
                "meals": "Breakfast & Dinner",
                "stay": "Hotel in Manali"
            },
            {
                "day": 5,
                "title": "Kasol & Manikaran Sahib Hot Springs",
                "desc": "Drive through the magical Parvati Valley into Kasol. Explore the riverside trails and quaint Israeli cafes. Visit the historic Manikaran Sahib Gurudwara and dip in the rejuvenating natural sulphur hot springs. Board evening return Volvo to Delhi.",
                "meals": "Breakfast",
                "stay": "Overnight Volvo bus"
            },
            {
                "day": 6,
                "title": "Delhi Arrival & Connecting Home",
                "desc": "Reach Delhi by 8:00 AM. Connect to flights/trains back to Hyderabad with a heart full of Himalayan memories.",
                "meals": "None",
                "stay": "Return journey"
            }
        ]),
        "inclusions": json.dumps([
            "Delhi to Shimla & Manali to Delhi in AC Volvo luxury coach",
            "1 Night hotel stay in Shimla, 3 Nights hotel stay in Manali",
            "Daily delicious Breakfast during hotel stays",
            "All internal transfers and sightseeing in private vehicle",
            "Experienced HappyMiles trip coordinator support throughout",
            "Toll, parking, and driver allowances included"
        ]),
        "exclusions": json.dumps([
            "Hyderabad to Delhi travel tickets (available on request)",
            "Lunches and dinners not mentioned",
            "Entry tickets to monuments & snow adventure activity charges",
            "Atal Tunnel / Sissu permit & taxi addon (subject to weather)",
            "Personal expenses & heater charges if requested at hotel"
        ]),
        "pickup_points": "Delhi Majnu Ka Tila / Kashmiri Gate (Hyderabad train/flight coordination provided)",
        "best_season": "October to June (Snow in Dec-Feb, pleasant summer in Mar-Jun)",
        "cancellation_policy": "Full refund 10 days prior. 50% refund 4-9 days prior. No refund within 72 hours.",
        "image_card": "/static/images/places/shimla-manali/shimla-manali-poster-900w.webp",
        "image_hero": "/static/images/places/shimla-manali/manali-temple-peaks.webp",
        "gallery_images": json.dumps([
            "/static/images/places/shimla-manali/shimla-manali-poster.webp",
            "/static/images/places/shimla-manali/shimla-ridge.webp",
            "/static/images/places/shimla-manali/kasol-valley.webp",
            "/static/images/places/shimla-manali/manikaran-springs.webp",
            "/static/images/places/shimla-manali/manali-temple-peaks.webp"
        ])
    }
]

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if packages exist
        existing = db.query(Package).count()
        if existing == 0:
            for p_data in PACKAGES_SEED:
                pkg = Package(**p_data)
                db.add(pkg)
            db.commit()
            print(f"Database initialized with {len(PACKAGES_SEED)} authentic packages!")
        else:
            print(f"Database already contains {existing} packages.")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
