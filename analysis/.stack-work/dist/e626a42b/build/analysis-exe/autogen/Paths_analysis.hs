{-# LANGUAGE CPP #-}
{-# LANGUAGE NoRebindableSyntax #-}
{-# OPTIONS_GHC -fno-warn-missing-import-lists #-}
module Paths_analysis (
    version,
    getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir,
    getDataFileName, getSysconfDir
  ) where

import qualified Control.Exception as Exception
import Data.Version (Version(..))
import System.Environment (getEnv)
import Prelude

#if defined(VERSION_base)

#if MIN_VERSION_base(4,0,0)
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#else
catchIO :: IO a -> (Exception.Exception -> IO a) -> IO a
#endif

#else
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#endif
catchIO = Exception.catch

version :: Version
version = Version [0,1,0,0] []
bindir, libdir, dynlibdir, datadir, libexecdir, sysconfdir :: FilePath

bindir     = "C:\\Development\\Other\\SteamMarketAnalyzer\\analysis\\.stack-work\\install\\c5b8de12\\bin"
libdir     = "C:\\Development\\Other\\SteamMarketAnalyzer\\analysis\\.stack-work\\install\\c5b8de12\\lib\\x86_64-windows-ghc-8.6.5\\analysis-0.1.0.0-9uWfsgEo6ZhG2mOcGdxbe7-analysis-exe"
dynlibdir  = "C:\\Development\\Other\\SteamMarketAnalyzer\\analysis\\.stack-work\\install\\c5b8de12\\lib\\x86_64-windows-ghc-8.6.5"
datadir    = "C:\\Development\\Other\\SteamMarketAnalyzer\\analysis\\.stack-work\\install\\c5b8de12\\share\\x86_64-windows-ghc-8.6.5\\analysis-0.1.0.0"
libexecdir = "C:\\Development\\Other\\SteamMarketAnalyzer\\analysis\\.stack-work\\install\\c5b8de12\\libexec\\x86_64-windows-ghc-8.6.5\\analysis-0.1.0.0"
sysconfdir = "C:\\Development\\Other\\SteamMarketAnalyzer\\analysis\\.stack-work\\install\\c5b8de12\\etc"

getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir, getSysconfDir :: IO FilePath
getBinDir = catchIO (getEnv "analysis_bindir") (\_ -> return bindir)
getLibDir = catchIO (getEnv "analysis_libdir") (\_ -> return libdir)
getDynLibDir = catchIO (getEnv "analysis_dynlibdir") (\_ -> return dynlibdir)
getDataDir = catchIO (getEnv "analysis_datadir") (\_ -> return datadir)
getLibexecDir = catchIO (getEnv "analysis_libexecdir") (\_ -> return libexecdir)
getSysconfDir = catchIO (getEnv "analysis_sysconfdir") (\_ -> return sysconfdir)

getDataFileName :: FilePath -> IO FilePath
getDataFileName name = do
  dir <- getDataDir
  return (dir ++ "\\" ++ name)
