mageia-custom-rpms
==================

Backported and custom Mageia RPMs

The work here, custom or otherwise is mostly (or exactly) derived from the Mageia SVN (http://svnweb.mageia.org/).

That said - the work is basically in 2 categories/folders.

* cauldron - rpms backported directly from a newer version of Mageia or Cauldron without changes
* custom - rpms that have been altered or writen fresh, including newer versions of existing packages

## RPM Access
Please note that all rpms are provided as is and without warranty. Here be dragons. May feast upon your youngest child.

However - we like dragons and in many cases use these rpms in production ourselves.

### Adding repos
#### Mageia 2
```
    urpmi.addmedia --distrib rsync://cyprix.com.au/rpm/Mga2
```
#### Mageia 3
```
    urpmi.addmedia --distrib rsync://cyprix.com.au/rpm/Mga3
```
#### Mageia 1 (no longer supported upstream)
```
    urpmi.addmedia --distrib rsync://cyprix.com.au/rpm/Mga1
```
