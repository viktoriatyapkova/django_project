create extension if not exists "uuid-ossp";

drop table if exists shops, marketplaces, shops_to_marketplaces, discounts cascade;

create table shops
(
    id         uuid primary key default uuid_generate_v4(),
    title text,
    description  text,
    rating float
);

create table marketplaces
(
    id          uuid primary key default uuid_generate_v4(),
    title       text,
    url_address text
);

create table shops_to_marketplaces
(
    shops_id  uuid references shops,
    marketplaces_id   uuid references marketplaces,
    primary key (shops_id, marketplaces_id)
);

create table discounts
(
	id uuid primary key default uuid_generate_v4(),
	shop_id uuid references shops,
	title text,
	description text,
	start_date date,
	end_date date
);

insert into shops(title, description, rating)
values ('Tech Haven', 'Your one-stop shop for all things tech! We offer a wide selection of laptops, smartphones, tablets, and accessories from top brands at competitive prices.', 4.8),
       ('HomeStyle', 'Discover stylish and affordable furniture, decor, and essentials for every room in your home. Create a space you love with HomeStyle!', 4.6),
       ('Fashion Forward', 'Stay ahead of the trends with our curated collection of clothing, shoes, and accessories for men and women. Shop the latest styles at Fashion Forward!', 4.7),
       ('Book Nook', 'Get lost in the world of books! We offer a diverse selection of genres, from bestsellers to classics, for readers of all ages.', 4.9),
       ('Sport Zone', 'Equip yourself for your active lifestyle! Find athletic apparel, footwear, equipment, and accessories for all your favorite sports and activities.', 4.5),
       ('Beauty Bar', 'Discover the latest beauty products and trends! We offer a wide range of makeup, skincare, haircare, and fragrance from top brands.', 4.6),
       ('Toy Box', 'Spark imagination and playtime fun! We offer a wide selection of toys, games, and activities for children of all ages.', 4.7),
       ('Pet Palace', 'Pamper your furry friends with everything they need! Find premium pet food, treats, toys, and accessories at Pet Palace.', 4.8),
       ('Garden Oasis', 'Create your own backyard paradise! We offer a variety of plants, seeds, gardening tools, and outdoor living essentials.', 4.5),
       ('Kitchen Essentials', 'Equip your kitchen with quality cookware, bakeware, appliances, and gadgets. Find everything you need for cooking and entertaining at Kitchen Essentials.', 4.6),
       ('Craft Corner', 'Unleash your creativity! Explore our selection of art supplies, crafting materials, and DIY project kits for all skill levels.', 4.7),
       ('Music Room', 'Discover a world of music! We offer a variety of instruments, audio equipment, sheet music, and accessories for musicians of all levels.', 4.8),
       ('Travel Gear', 'Get ready for your next adventure! Find luggage, travel accessories, and outdoor gear for your journeys near and far.', 4.5),
       ('Eco-Friendly Finds', 'Shop sustainably with our selection of eco-conscious products for your home, lifestyle, and personal care.', 4.9),
       ('Party Supplies Plus', 'Celebrate in style! Find everything you need for birthdays, holidays, and special occasions, from decorations to party favors.', 4.6),
       ('Gadget Geek', 'Discover the latest and coolest gadgets, from smart home devices to innovative tech accessories.', 4.7),
       ('Cozy Comfort', 'Find luxurious bedding, bath linens, and home textiles to create a relaxing and comfortable atmosphere.', 4.8),
       ('Artistic Flair', 'Explore a unique collection of art prints, paintings, sculptures, and home decor to add a touch of creativity to your space.', 4.6),
       ('Foodie Delights', 'Indulge in gourmet food, snacks, and beverages from around the world. Discover new flavors and culinary experiences.', 4.9),
       ('WellFit Essentials', 'Shop for fitness equipment, activewear, and wellness products to support your healthy lifestyle.', 4.5),
       ('Jewelry Box', 'Find exquisite jewelry pieces, from classic designs to trendy statement pieces, for every occasion.', 4.7),
       ('Kiddie Corner', 'Shop for children''s clothing, shoes, and accessories with adorable styles and comfortable fits.', 4.6),
       ('Stationery Studio', 'Discover stylish notebooks, journals, pens, and desk accessories to add a touch of personality to your workspace.', 4.8),
       ('Hobby Haven', 'Find supplies and kits for all your hobbies, from model building to painting to knitting and more.', 4.5),
       ('Gift Gallery', 'Find the perfect gifts for everyone on your list, with a wide selection of unique and thoughtful items.', 4.7);

insert into marketplaces(title, url_address)
values ('Bazaar Global', 'bazaar.global'),
       ('Emporium Connect', 'emporiumconnect.com'),
       ('Trade Nexus', 'tradenexus.net'),
       ('Vendora Collective', 'vendora.co'),
       ('Market Bridge', 'marketbridge.io');

insert into shops_to_marketplaces(shops_id, marketplaces_id)
values
    ((select id from shops where title = 'Tech Haven'),
     (select id from marketplaces where title = 'Bazaar Global')),
    ((select id from shops where title = 'HomeStyle'),
     (select id from marketplaces where title = 'Bazaar Global')),
    ((select id from shops where title = 'Fashion Forward'),
     (select id from marketplaces where title = 'Bazaar Global')),
    ((select id from shops where title = 'Book Nook'),
     (select id from marketplaces where title = 'Bazaar Global')),
    ((select id from shops where title = 'Sport Zone'),
     (select id from marketplaces where title = 'Bazaar Global')),
    ((select id from shops where title = 'Beauty Bar'),
     (select id from marketplaces where title = 'Bazaar Global')),
    ((select id from shops where title = 'Toy Box'),
     (select id from marketplaces where title = 'Bazaar Global')),
    ((select id from shops where title = 'Pet Palace'),
     (select id from marketplaces where title = 'Bazaar Global')),
    ((select id from shops where title = 'Garden Oasis'),
     (select id from marketplaces where title = 'Bazaar Global')),
    ((select id from shops where title = 'Kitchen Essentials'),
     (select id from marketplaces where title = 'Bazaar Global')),
    ((select id from shops where title = 'Craft Corner'),
     (select id from marketplaces where title = 'Emporium Connect')),
    ((select id from shops where title = 'Music Room'),
     (select id from marketplaces where title = 'Emporium Connect')),
    ((select id from shops where title = 'Travel Gear'),
     (select id from marketplaces where title = 'Emporium Connect')),
    ((select id from shops where title = 'Eco-Friendly Finds'),
     (select id from marketplaces where title = 'Emporium Connect')),
    ((select id from shops where title = 'Party Supplies Plus'),
     (select id from marketplaces where title = 'Emporium Connect')),
    ((select id from shops where title = 'Gadget Geek'),
     (select id from marketplaces where title = 'Emporium Connect')),
    ((select id from shops where title = 'Cozy Comfort'),
     (select id from marketplaces where title = 'Emporium Connect')),
    ((select id from shops where title = 'Artistic Flair'),
     (select id from marketplaces where title = 'Emporium Connect')),
    ((select id from shops where title = 'Foodie Delights'),
     (select id from marketplaces where title = 'Emporium Connect')),
    ((select id from shops where title = 'WellFit Essentials'),
     (select id from marketplaces where title = 'Emporium Connect')),
    ((select id from shops where title = 'Jewelry Box'),
     (select id from marketplaces where title = 'Trade Nexus')),
    ((select id from shops where title = 'Kiddie Corner'),
     (select id from marketplaces where title = 'Trade Nexus')),
    ((select id from shops where title = 'Stationery Studio'),
     (select id from marketplaces where title = 'Trade Nexus')),
    ((select id from shops where title = 'Hobby Haven'),
     (select id from marketplaces where title = 'Trade Nexus')),
    ((select id from shops where title = 'Gift Gallery'),
     (select id from marketplaces where title = 'Trade Nexus')),
    ((select id from shops where title = 'Tech Haven'),
     (select id from marketplaces where title = 'Trade Nexus')),
    ((select id from shops where title = 'HomeStyle'),
     (select id from marketplaces where title = 'Trade Nexus')),
    ((select id from shops where title = 'Fashion Forward'),
     (select id from marketplaces where title = 'Trade Nexus')),
    ((select id from shops where title = 'Book Nook'),
     (select id from marketplaces where title = 'Trade Nexus')),
    ((select id from shops where title = 'Sport Zone'),
     (select id from marketplaces where title = 'Trade Nexus')),
    ((select id from shops where title = 'Beauty Bar'),
     (select id from marketplaces where title = 'Vendora Collective')),
    ((select id from shops where title = 'Toy Box'),
     (select id from marketplaces where title = 'Vendora Collective')),
    ((select id from shops where title = 'Pet Palace'),
     (select id from marketplaces where title = 'Vendora Collective')),
    ((select id from shops where title = 'Garden Oasis'),
     (select id from marketplaces where title = 'Vendora Collective')),
    ((select id from shops where title = 'Kitchen Essentials'),
     (select id from marketplaces where title = 'Vendora Collective')),
    ((select id from shops where title = 'Craft Corner'),
     (select id from marketplaces where title = 'Vendora Collective')),
    ((select id from shops where title = 'Music Room'),
     (select id from marketplaces where title = 'Vendora Collective')),
    ((select id from shops where title = 'Travel Gear'),
     (select id from marketplaces where title = 'Vendora Collective')),
    ((select id from shops where title = 'Eco-Friendly Finds'),
     (select id from marketplaces where title = 'Vendora Collective')),
    ((select id from shops where title = 'Party Supplies Plus'),
     (select id from marketplaces where title = 'Vendora Collective')),
    ((select id from shops where title = 'Gadget Geek'),
     (select id from marketplaces where title = 'Market Bridge')),
    ((select id from shops where title = 'Cozy Comfort'),
     (select id from marketplaces where title = 'Market Bridge')),
    ((select id from shops where title = 'Artistic Flair'),
     (select id from marketplaces where title = 'Market Bridge')),
    ((select id from shops where title = 'Foodie Delights'),
     (select id from marketplaces where title = 'Market Bridge')),
    ((select id from shops where title = 'WellFit Essentials'),
     (select id from marketplaces where title = 'Market Bridge')),
    ((select id from shops where title = 'Jewelry Box'),
     (select id from marketplaces where title = 'Market Bridge')),
    ((select id from shops where title = 'Kiddie Corner'),
     (select id from marketplaces where title = 'Market Bridge')),
    ((select id from shops where title = 'Stationery Studio'),
     (select id from marketplaces where title = 'Market Bridge')),
    ((select id from shops where title = 'Hobby Haven'),
     (select id from marketplaces where title = 'Market Bridge')),
    ((select id from shops where title = 'Gift Gallery'),
     (select id from marketplaces where title = 'Market Bridge'));
    

insert into discounts(shop_id, title, description, start_date, end_date) 
values  ((select id from shops where title = 'Tech Haven'), 'Back to School Tech Deals', 'Save up to 25% on laptops, tablets, and accessories for students of all ages.', '2024-08-01', '2024-08-15'),
    	((select id from shops where title = 'Tech Haven'), 'Holiday Gadget Gift Extravaganza', 'Enjoy special discounts and bundles on the latest tech gifts for everyone on your list.', '2023-11-15', '2023-12-24'),
    	((select id from shops where title = 'HomeStyle'), 'Spring Refresh Sale', 'Update your home décor with 20% off furniture, rugs, and lighting.', '2024-03-01', '2024-04-30'),
    	((select id from shops where title = 'HomeStyle'), 'Summer Patio Savings', 'Get ready for outdoor entertaining with discounts on patio furniture, grills, and outdoor accessories.', '2022-05-15', '2022-07-31'),
    	((select id from shops where title = 'Fashion Forward'), 'Summer Style Sale', 'Enjoy 30% off on summer apparel, shoes, and accessories.', '2020-06-01', '2020-08-31'),
    	((select id from shops where title = 'Fashion Forward'), 'Fall Fashion Arrivals Event', 'Be the first to shop the latest fall styles and receive a 15% discount.', '2023-09-01', '2023-09-30'),
    	((select id from shops where title = 'Book Nook'), 'Summer Reading Challenge', 'Buy 3 books, get 1 free on select titles.', '2024-06-01', '2024-08-31'),
    	((select id from shops where title = 'Book Nook'), 'Holiday Book Gift Sets', 'Discover curated book gift sets for all ages at special prices.', '2023-11-01', '2023-12-24'),
    	((select id from shops where title = 'Sport Zone'), 'Get Fit for Summer Sale', '20% off on fitness equipment, activewear, and sports gear.', '2024-04-15', '2024-05-31'),
    	((select id from shops where title = 'Sport Zone'), 'Winter Sports Clearance', 'Save up to 50% on winter sports apparel, equipment, and accessories.', '2023-01-01', '2023-02-28'),
    	((select id from shops where title = 'Beauty Bar'), 'Spring Makeup Refresh', 'Enjoy 15% off on new makeup palettes and skincare products.', '2024-03-15', '2024-04-30'),
    	((select id from shops where title = 'Beauty Bar'), 'Holiday Beauty Gift Sets', 'Discover luxurious gift sets featuring top beauty brands at special prices.', '2022-11-01', '2022-12-24'),
    	((select id from shops where title = 'Toy Box'), 'Summer Playtime Fu', 'Buy 2 toys, get 1 free on select items', '2023-06-01', '2023-08-31'),
    	((select id from shops where title = 'Toy Box'), 'Holiday Toy Spectacular', 'Special discounts on popular toys and games for the holiday season.', '2024-11-15', '2024-12-01'),
    	((select id from shops where title = 'Pet Palace'), 'Spring Pet Pampering Event', '20% off on grooming supplies, pet beds, and spring-themed toys.', '2020-03-01', '2020-03-15'),
    	((select id from shops where title = 'Pet Palace'), 'Holiday Pet Gift Extravaganza', 'Spoil your furry friends with special discounts on holiday-themed treats, toys, and accessories.', '2023-11-15', '2023-12-24'),
    	((select id from shops where title = 'Garden Oasis'), 'Spring Planting Sale', '25% off on plants, seeds, and gardening tools', '2024-03-01', '2024-05-31'),
    	((select id from shops where title = 'Garden Oasis'), 'Fall Harvest Savings', 'Discounts on fall décor, bulbs, and gardening equipment.', '2022-09-01', '2022-10-31'),
    	((select id from shops where title = 'Gadget Geek'), 'Innovation Celebration', 'Discover cutting-edge gadgets with special discounts and early access to new releases.', '2020-10-01', '2920-10-31'),
    	((select id from shops where title = 'Gadget Geek'), 'Smart Home Upgrade Sale', 'Save on smart home devices, from security systems to voice assistants and lighting solutions.', '2023-11-01', '2023-11-30'),
    	((select id from shops where title = 'Cozy Comfort'), 'Winter Warm-Up Sale', 'Get cozy with discounts on blankets, throws, and flannel sheets.', '2023-11-01', '2023-12-31'),
    	((select id from shops where title = 'Cozy Comfort'), 'Spring Bedding Refresh', 'Update your bedroom with new bedding sets and duvet covers at special prices.', '2020-03-01', '2020-04-30'),
    	((select id from shops where title = 'Artistic Flair'), 'Artful Home Decor Sale', 'Add personality to your space with discounts on art prints, sculptures, and decorative accents.', '2023-05-01', '2023-05-31'),
    	((select id from shops where title = 'Artistic Flair'), 'Holiday Art Gift Collection', 'Find unique and artistic gifts for art lovers on your list.', '2022-11-01', '2022-12-24'),
    	((select id from shops where title = 'Foodie Delights'), 'Summer Grilling Favorites', 'Discover gourmet grilling essentials, sauces, and marinades at special prices.', '2023-05-15', '2023-07-31'),
    	((select id from shops where title = 'Foodie Delights'), 'Holiday Gourmet Gift Baskets', 'Indulge in curated gift baskets filled with gourmet treats and delicacies.', '2021-11-01', '2021-11-30'),
    	((select id from shops where title = 'WellFit Essentials'), 'Spring into Fitness', 'Get 20% off on fitness trackers, yoga mats, and workout apparel.', '2023-03-15', '2023-04-30'),
    	((select id from shops where title = 'WellFit Essentials'), 'Holiday Wellness Gift Sets', 'Discover curated gift sets featuring self-care essentials and wellness products.', '2023-11-30', '2023-12-24'),
    	((select id from shops where title = 'Music Room'), 'Back to School Music Deals', 'Save on instruments, music books, and accessories for students of all ages.', '2022-08-31', '2022-09-15'),
    	((select id from shops where title = 'Music Room'), 'Holiday Music Gift Extravaganza', 'Find the perfect musical gifts for everyone on your list with special discounts and bundles.', '2023-11-15', '2023-12-15'),
    	((select id from shops where title = 'Travel Gear'), 'Summer Vacation Essentials', 'Get 15% off on luggage, travel accessories, and guidebooks.', '2020-05-15', '2020-08-31'),
    	((select id from shops where title = 'Travel Gear'), 'Holiday Travel Deals', 'Discover travel packages and special offers for holiday getaways.', '2023-11-20', '2023-11-30'),
    	((select id from shops where title = 'Hobby Haven'), 'Back to School Art Supplies Sale', 'Stock up on art supplies with discounts on paints, brushes, and sketchbooks.', '2023-08-01', '2023-09-15'),
    	((select id from shops where title = 'Hobby Haven'), 'Holiday Craft Kits and Gifts', 'Explore a variety of craft kits and art supplies perfect for holiday gifts.', '2022-11-02', '2022-11-24'),
    	((select id from shops where title = 'Book Nook'), 'Summer Reading Escape', 'Enjoy 10% off on all fiction and non-fiction books.', '2022-06-01', '2022-08-31'),
    	((select id from shops where title = 'Book Nook'), 'Holiday Book Gift Guide', 'Discover a curated selection of books for everyone on your gift list.', '2023-11-11', '2023-11-19'),
    	((select id from shops where title = 'Jewelry Box'), 'Sparkling Summer Sale', 'Enjoy 20% off on all summer jewelry collections, including vibrant gemstone pieces and delicate gold necklaces.', '2024-05-31', '2024-06-22'),
    	((select id from shops where title = 'Jewelry Box'), 'Holiday Gift of Sparkle', 'Find the perfect gift for your loved ones with 15% off on all diamond and gemstone jewelry.', '2023-11-01', '2023-11-21'),
    	((select id from shops where title = 'Kiddie Corner'), 'Back to School Style', 'Get your little ones ready for school with 25% off on all backpacks, lunch boxes, and school uniforms.', '2024-08-31', '2024-09-15'),
    	((select id from shops where title = 'Kiddie Corner'), 'Holiday Dress-Up Fun', 'Find adorable holiday outfits and cozy pajamas for kids at 20% off.', '2023-11-21', '2023-12-12'),
    	((select id from shops where title = 'Stationery Studio'), 'Back to School Organization', 'Stay organized and stylish with 15% off on all notebooks, planners, and desk organizers.', '2024-08-01', '2024-08-15'),
    	((select id from shops where title = 'Stationery Studio'), 'Holiday Gifting Made Personal', 'Find unique and personalized gifts like custom notebooks, engraved pens, and stationery sets at 10% off.', '2023-12-01', '2023-12-15'),
    	((select id from shops where title = 'Hobby Haven'), 'Summer Creativity Boost', 'Unleash your creativity with 20% off on all art supplies, craft kits, and hobby tools.', '2022-07-08', '2022-07-29'),
    	((select id from shops where title = 'Hobby Haven'), 'Holiday Hobby Gift Guide ', 'Find the perfect gift for the hobbyist in your life with 15% off on all model kits, painting supplies, and crafting tools.', '2020-10-31', '2020-11-10'),
    	((select id from shops where title = 'Gift Gallery'), 'Summer Gift Giving', 'Find unique and thoughtful gifts for any occasion with 10% off on all items in the store.', '2024-06-01', '2024-06-11'),
    	((select id from shops where title = 'Gift Gallery'), 'Holiday Gift Extravaganza', 'Discover a wide selection of gifts for everyone on your list at special holiday prices with discounts up to 25%.', '2023-12-20', '2024-01-10'),
    	((select id from shops where title = 'Eco-Friendly Finds'), 'Act Now for the Planet', 'Enjoy 20% off all reusable products in-store and online.', '2024-04-22', '2024-05-05'),
    	((select id from shops where title = 'Eco-Friendly Finds'), 'Green Your Routine', 'Buy 2 eco-friendly cleaning products, get 1 free!', '2024-05-10', '2024-05-31'),
    	((select id from shops where title = 'Party Supplies Plus'), 'Birthday Bash Bonanza', 'Get 15% off all birthday party decorations and supplies.', '2024-06-01', '2024-06-15'),
    	((select id from shops where title = 'Party Supplies Plus'), 'Seasonal Savings Spectacular', 'Stock up on holiday decor with buy one, get one 50% off on select items.', '2023-11-01', '2023-11-30');

