from injector import Module, provider

from api.google.sheet_client import GoogleSheetsClient
from api.supabase.repo.common_repo import CommonRepository
from api.supabase.repo.entrance_repo import EntranceRepository
from api.supabase.repo.peer_repo import PeerRepository
from api.supabase.repo.score_repo import ScoreRepository
from command import Commander
from layout import Euljiro
from service.batch_score import BatchMgr
from service.common_service import CommonMgr
from service.consume_point import PointMgr
from service.nfc_service import NfcService
from service.room_stay_service import EnterMgr, ExitMgr, ScoreMgr

class ChungMuro(Module):

    @provider
    def provide_entrance_repository(self) -> EntranceRepository:
        return EntranceRepository()

    @provider
    def provide_common_repository(self) -> CommonRepository:
        return CommonRepository()

    @provider
    def provide_score_repository(self) -> ScoreRepository:
        return ScoreRepository()

    @provider
    def provide_peer_repository(self) -> PeerRepository:
        return PeerRepository()

    @provider
    def provide_enter_mgr(self,
                          entrance_repo: EntranceRepository,
                          common_repo: CommonRepository,
                          score_repo: ScoreRepository) -> EnterMgr:
        return EnterMgr(entrance_repo, common_repo, score_repo)

    @provider
    def provide_exit_mgr(self, entrance_repo: EntranceRepository) -> ExitMgr:
        return ExitMgr(entrance_repo)

    @provider
    def provide_score_mgr(self,
                          score_repo: ScoreRepository,
                          common_repo: CommonRepository,
                          google_sheet_client: GoogleSheetsClient) -> ScoreMgr:
        return ScoreMgr(score_repo, common_repo, google_sheet_client)

    @provider
    def provide_common_mgr(self, common_repo: CommonRepository, peer_repo: PeerRepository) -> CommonMgr:
        return CommonMgr(common_repo, peer_repo)

    @provider
    def provide_nfc_service(self) -> NfcService:
        return NfcService()

    @provider
    def provide_point_mgr(self, score_repo: ScoreRepository) -> PointMgr:
        return PointMgr(score_repo)

    @provider
    def provide_batch_mgr(self, entrance_repo: EntranceRepository, score_repo: ScoreRepository) -> BatchMgr:
        return BatchMgr(entrance_repo, score_repo)

    @provider
    def provide_command(self,
                            enter_mgr: EnterMgr,
                            exit_mgr:ExitMgr,
                            score_mgr:ScoreMgr,
                            common_mgr:CommonMgr,
                            nfc_mgr:NfcService,
                            eul:Euljiro,
                            point_mgr:PointMgr,
                            batch_mgr:BatchMgr
                            ) -> Commander:
        return Commander(enter_mgr, exit_mgr, score_mgr, common_mgr, nfc_mgr, eul, point_mgr, batch_mgr)

