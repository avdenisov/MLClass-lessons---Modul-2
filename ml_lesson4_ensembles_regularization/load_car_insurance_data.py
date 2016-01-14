def load_train_and_test(path_to_train, path_to_test):
    # read data into pandas data frames
    train_df = pd.read_csv(path_to_train,
                           header=0, index_col=0)
    test_df = pd.read_csv(path_to_test,
                          header=0, index_col=0)

    def extract_region(auto_number):
        """
        Returns region based on the auto number
        X796TH96RUS -> 96
        E432XX77RUS -> 77
        If there are more than 2-3 digits before 'RUS', 
        returns "not-auto-num"
        """
        index = auto_number.rindex("RUS") - 1
        while auto_number[index].isdigit():
            index -= 1
        auto_number = auto_number[index + 1 :auto_number.rindex('RUS')]
        return auto_number if len(auto_number) <= 3 else "not-auto-num"

    # auto brand and too_much are categorical so we encode these columns
    # ex: "Volvo" -> 1, "Audi" -> 2 etc
    auto_brand_encoder = preprocessing.LabelEncoder()
    auto_brand_encoder.fit(train_df['auto_brand'])
    target_encoder = preprocessing.LabelEncoder()
    target_encoder.fit(train_df['too_much'])
    region_encoder = preprocessing.LabelEncoder()
    regions_train = train_df['auto_number'].apply(extract_region)
    region_encoder.fit(regions_train)

    train_df['region'] = region_encoder\
                        .transform(regions_train)
    train_df['auto_brand'] = auto_brand_encoder\
                            .transform(train_df['auto_brand'])

    # form a numpy array to fit as train set labels
    y = train_df['too_much']

    train_df = train_df.drop(['auto_number', 'too_much'], axis=1)

    test_df['region'] = region_encoder\
                        .transform(test_df['auto_number']\
                                   .apply(extract_region))
    test_df['auto_brand'] = auto_brand_encoder\
                            .transform(test_df['auto_brand'])
    test_df = test_df.drop('auto_number', axis=1)
    return train_df, y, test_df