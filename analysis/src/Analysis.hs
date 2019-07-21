module Analysis
(
    suggestedAction,
    Action
)
where
    import Trend;

    data Action = Buy | Sell | Ignore deriving (Show);

    suggestedAction :: Int -> [Double] -> Action
    suggestedAction volume (x:xs)
        | volume < 8 = Ignore
        | otherwise =
            case direction of 
                Nothing -> Ignore
                Just Up -> Sell
                Just Down -> Buy
            where direction = fluctuation (x:xs)