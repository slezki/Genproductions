# cfg file for X(10700) -> Ups(2S) pion0. Masses and widths are matched between pythia, evtgen and PDG 2016

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('myX'),
            operates_on_particles = cms.vint32(200553),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Particle Upsilon 9.4603000 0.00005402
Particle Upsilon(2S) 10.023260 0.00003198
Particle Upsilon(3S) 10.700000 0.00000

Alias myUpsilon Upsilon
Alias myUpsilon2S Upsilon(2S)
Alias myX Upsilon(3S)

Decay myUpsilon
1.0   mu+  mu-          PHOTOS  VLL;
Enddecay

Decay myUpsilon2S
1.0   myUpsilon pi+ pi-  PHSP;
Enddecay

Decay pi0
1.0   gamma   gamma  PHSP;
Enddecay

Decay myX
1.0   myUpsilon2S  pi0   PHSP;
Enddecay

End
"""
            )
	),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
	pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'Bottomonium:states(3S1) = 200553',
            'Bottomonium:O(3S1)[3S1(1)] = 3.54',
            'Bottomonium:O(3S1)[3S1(8)] = 0.075',
            'Bottomonium:O(3S1)[1S0(8)] = 0.1',
            'Bottomonium:O(3S1)[3P0(8)] = 0.1',
            'Bottomonium:gg2bbbar(3S1)[3S1(1)]g = on',
            'Bottomonium:gg2bbbar(3S1)[3S1(8)]g = on',
            'Bottomonium:qg2bbbar(3S1)[3S1(8)]q = on',
            'Bottomonium:qqbar2bbbar(3S1)[3S1(8)]g = on',
            'Bottomonium:gg2bbbar(3S1)[1S0(8)]g = on',
            'Bottomonium:qg2bbbar(3S1)[1S0(8)]q = on',
            'Bottomonium:qqbar2bbbar(3S1)[1S0(8)]g = on',
            'Bottomonium:gg2bbbar(3S1)[3PJ(8)]g = on',
            'Bottomonium:qg2bbbar(3S1)[3PJ(8)]q = on',
            'Bottomonium:qqbar2bbbar(3S1)[3PJ(8)]g = on',
            'Bottomonium:gg2bbbar(3S1)[3S1(1)]gm = on',
            'PhaseSpace:pTHatMin = 2.',
            '200553:m0 = 10.700000',
            '200553:onMode = off'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters'
                                    )
    )
)

# We will filter for X_b, and chi_b1, first on the ID, then in the mass, this will constraint the photon daughter

ups2SIDfilter = cms.EDFilter("MCSingleParticleFilter",
    ParticleID = cms.untracked.vint32(100553),
    MinPt = cms.untracked.vdouble(2.0),
    MinEta = cms.untracked.vdouble(-2.4),
    MaxEta = cms.untracked.vdouble(2.4),
    Status = cms.untracked.vint32(2)
)

upsIDfilter = cms.EDFilter("MCSingleParticleFilter",
    ParticleID = cms.untracked.vint32(553),
    MinPt = cms.untracked.vdouble(2.0),
    MinEta = cms.untracked.vdouble(-2.4),
    MaxEta = cms.untracked.vdouble(2.4),
    Status = cms.untracked.vint32(2)
)

# Next two muon filter are derived from muon reconstruction

muonsfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(100553),
    MinPt = cms.untracked.vdouble(1.0,1.0),
    ParticleID = cms.untracked.int32(553),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.4,-2.4),
    MaxEta = cms.untracked.vdouble(2.4,2.4),
    NumberDaughters = cms.untracked.int32(2),
    DaughterIDs = cms.untracked.vint32(-13,13)
)

pionsfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(200553),
    MinPt = cms.untracked.vdouble(0.0,0.0),
    ParticleID = cms.untracked.int32(100553),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.4,-2.4),
    MaxEta = cms.untracked.vdouble(2.4,2.4),
    NumberDaughters = cms.untracked.int32(2),
    DaughterIDs = cms.untracked.vint32(-211,211)
)


ProductionFilterSequence = cms.Sequence(generator*ups2SIDfilter*upsIDfilter*muonsfilter*pionsfilter)