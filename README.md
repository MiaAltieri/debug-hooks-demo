### Meeting Notes

(3 mins)
- Explain Charm Code

(6 mins)
- Demonstrate why we would want to use Debug hooks
- Build and Deploy Charm
```
charmcraft pack
juju deploy ./*charm -n2
```
- Watch Charm in separate terminal
```
watch -n1 --color juju status --color
```
- Debug logs in separate terminal
```
juju debug-logs
```
- See it fail in `juju-watch`
    - Explain that we could re-write the code, re-pack, re-deploy to fix this which would take **awhile** OR we could do a juju debug-hooks session and fix it there

```
juju debug-hooks awesome/<failing unit number>
```
- Get hooks to re-fire (separate terminal)
```
juju resolved awesome/<failing unit number>
```
- In debug-hooks session terminal run the code and edit file
```
./dispatch
vi src/charm
# change line 48 to useful_math = unit_number/10 
# exit vi
# re-run code and see that it works
./dispatch
exit
```

(6 mins)
- Now demonstrate that debug hooks can be useful for testing different executation scenarios (in a new terminal session) 
```
# add unit
juju add-unit awesome

# run debug-hooks for the start hook of new unit
juju debug-hooks awesome/<new unit number> start
```

- In the terminal with juju debug hooks session for the leader 
```
# if update status hook is visible at bottom of the screen do the following until you see awesome-relation-joined
./dispatch
exit
```
- Once we see awesome-relation-joined at the bottom do:
```
./dispatch # this will give us an error since we haven't executed the start hook in the other juju debug-hooks session
```
- In terminal with new unit do:
```
# for start hook
./dispatch
exit
```
- In terminal for leader unit now do 
```
./dispatch
```
and we see theat the code works, this is how juju debug hooks can be used to test asynchronous situations.

Now we change to Liam and have him discuss useful [primatives](https://discourse.charmhub.io/t/hook-tools/1163), such as `relation-get`, `relation-set`, `config-get`, `network-get`. (Note these are done within the `juju debug-hooks` session)
