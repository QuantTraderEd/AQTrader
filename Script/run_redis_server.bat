@echo on
title redis server
mode con cols=120 lines=22
c:
cd c:\Redis-x64-2.8.2103
cmd /K redis-server.exe redis.conf