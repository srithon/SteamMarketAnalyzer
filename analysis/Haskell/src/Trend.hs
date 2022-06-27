module Trend
(
    Direction(..),
    fluctuation,
    percentError
)
where
    import Data.Function;

    data Direction = Up | Down deriving (Show);

    -- premise is that starting values get more weighting than ending values.
    -- the way we accomplish this is by distributing weightings from the range [1..0] evenly across the list.
    -- we can accomplish this by getting the interval: (1 / (n + 1)), and creating the weights by subtracting this from 1
    weightedAverage :: [Double] -> Double
    weightedAverage ls = (/ fromIntegral len) $ sum $ zipWith (*) ls $ weightingList len
      where
        len = length ls

    -- given a list, yields the list of weightings to use.
    -- did it this way so that the first one would not be 1.0
    weightingList :: Int -> [Double]
    weightingList len = take len $ drop 1 [1, 1 - interval ..]
      where
        interval = 1 / fromIntegral (len + 1)

    percentError :: Double -> Double -> Double
    percentError a b = ((a - b) / b) * 100

    fluctuationFirstToRest :: [Double] -> Double
    fluctuationFirstToRest (x:xs) = percentError x (weightedAverage xs)

    fluctuation :: [Double] -> Maybe Direction
    fluctuation (x:xs) = fluctuationDirection $ fluctuationFirstToRest (x:xs)

    fluctuationDirection :: Double -> Maybe Direction
    fluctuationDirection f
        | f > 15 = Just Up
        | f < -15 = Just Down
        | otherwise = Nothing

    {-

    (1 - (1 * 0.2))x +
    (1 - (2 * 0.2))x-1 +
    (1 - (3 * 0.2))x-2 +
    (1 - (4 * 0.2))x-3 

    0.8 + 0.6 + 0.4 + 0.2 = 2

    1 - 1 * 0.1 +
    1 - 2 * 0.1 +
    1 - 3 * 0.1 +
    1 - 4 * 0.1 +
    1 - 5 * 0.1 +
    1 - 6 * 0.1 +
    1 - 7 * 0.1 +
    1 - 8 * 0.1 +
    1 - 9 * 0.1

    0.9 + 0.8 + 0.7 + 0.6 + 0.5 + 0.4 + 0.3 + 0.2 + 0.1 = 4.5

    -}
