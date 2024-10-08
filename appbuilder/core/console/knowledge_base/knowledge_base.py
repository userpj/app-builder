# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import uuid
from pydantic import BaseModel
from pydantic import Field
from typing import Union
from typing import Optional
from appbuilder.core._client import HTTPClient
from appbuilder.core.console.knowledge_base import data_class
from appbuilder.core.component import Message, Component
from appbuilder.utils.func_utils import deprecated
from appbuilder.utils.trace.tracer_wrapper import client_tool_trace


class KnowledgeBase(Component):

    def __init__(
        self,
        knowledge_id: Optional[str] = None,
        knowledge_name: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.knowledge_id = knowledge_id
        self.knowledge_name = knowledge_name

    @classmethod
    @deprecated()
    def create_knowledge(cls, knowledge_name: str) -> "KnowledgeBase":
        """
        Deprecated: use create_knowledge_base instead
        """
        payload = json.dumps({"name": knowledge_name})
        http_client = HTTPClient()
        headers = http_client.auth_header()
        headers["Content-Type"] = "application/json"
        create_url = "/v1/ai_engine/agi_platform/v1/datasets/create"
        response = http_client.session.post(
            url=http_client.service_url(create_url), headers=headers, data=payload
        )
        http_client.check_response_header(response)
        http_client.check_console_response(response)
        response = response.json()["result"]
        return KnowledgeBase(
            knowledge_id=response["id"], knowledge_name=response["name"]
        )

    def upload_file(
        self, file_path: str, client_token: str = None
    ) -> data_class.KnowledgeBaseUploadFileResponse:
        if not os.path.exists(file_path):
            raise FileNotFoundError("File {} does not exist".format(file_path))

        headers = self.http_client.auth_header_v2()
        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2("/file", client_token=client_token)

        with open(file_path, "rb") as f:
            multipart_form_data = {"file": (os.path.basename(file_path), f)}

            response = self.http_client.session.post(
                url=url,
                headers=headers,
                files=multipart_form_data,
            )

            self.http_client.check_response_header(response)
            self.http_client.check_console_response(response)
            data = response.json()
            resp = data_class.KnowledgeBaseUploadFileResponse(**data)

        return resp

    def add_document(
        self,
        content_type: str,
        file_ids: list[str] = [],
        is_enhanced: bool = False,
        custom_process_rule: Optional[data_class.CustomProcessRule] = None,
        knowledge_base_id: Optional[str] = None,
        client_token: str = None,
    ) -> data_class.KnowledgeBaseAddDocumentResponse:
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledge_base/document", client_token=client_token
        )

        request = data_class.KnowledgeBaseAddDocumentRequest(
            knowledge_base_id=knowledge_base_id or self.knowledge_id,
            content_type=content_type,
            file_ids=file_ids,
            is_enhanced=is_enhanced,
            custom_process_rule=custom_process_rule,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseAddDocumentResponse(**data)
        return resp

    def delete_document(
        self,
        document_id: str,
        knowledge_base_id: Optional[str] = None,
        client_token: str = None,
    ) -> data_class.KnowledgeBaseDeleteDocumentResponse:
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledge_base/document", client_token=client_token
        )
        request = data_class.KnowledgeBaseDeleteDocumentRequest(
            knowledge_base_id=knowledge_base_id or self.knowledge_id,
            document_id=document_id,
        )
        response = self.http_client.session.delete(
            url=url, headers=headers, params=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseDeleteDocumentResponse(**data)
        return resp

    def get_documents_list(
        self,
        limit: int = 10,
        after: Optional[str] = "",
        before: Optional[str] = "",
        knowledge_base_id: Optional[str] = None,
    ) -> data_class.KnowledgeBaseGetDocumentsListResponse:
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2("/knowledge_base/documents")
        request = data_class.KnowledgeBaseGetDocumentsListRequest(
            knowledge_base_id=knowledge_base_id or self.knowledge_id,
            limit=limit,
            after=after,
            before=before,
        )
        response = self.http_client.session.get(
            url=url, headers=headers, params=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseGetDocumentsListResponse(**data)
        return resp

    def create_knowledge_base(
        self,
        name: str,
        description: str,
        type: str = "public",
        esUrl: str = None,
        esUserName: str = None,
        esPassword: str = None,
        client_token: str = None,
    ) -> data_class.KnowledgeBaseDetailResponse:
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=CreateKnowledgeBase", client_token=client_token
        )

        request = data_class.KnowledgeBaseCreateKnowledgeBaseRequest(
            name=name,
            description=description,
            config={
                "index": {
                    "type": type,
                    "esUrl": esUrl,
                    "username": esUserName,
                    "password": esPassword,
                }
            },
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseDetailResponse(**data)
        self.knowledge_id = resp.id
        self.knowledge_name = resp.name
        return resp

    def get_knowledge_base_detail(
        self, knowledge_base_id: Optional[str] = None
    ) -> data_class.KnowledgeBaseDetailResponse:
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )

        request = data_class.KnowledgeBaseGetDetailRequest(
            id=knowledge_base_id or self.knowledge_id
        )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=DescribeKnowledgeBase"
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseDetailResponse(**data)
        return resp

    def modify_knowledge_base(
        self,
        knowledge_base_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        client_token: str = None,
    ):
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )
        request = data_class.KnowledgeBaseModifyRequest(
            id=knowledge_base_id or self.knowledge_id,
            name=name,
            description=description,
        )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=ModifyKnowledgeBase", client_token=client_token
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def delete_knowledge_base(
        self, knowledge_base_id: Optional[str] = None, client_token: str = None
    ):
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )
        request = data_class.KnowledgeBaseDeleteRequest(
            id=knowledge_base_id or self.knowledge_id
        )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=DeleteKnowledgeBase", client_token=client_token
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def create_documents(
        self,
        id: Optional[str] = None,
        contentFormat: str = "",
        source: data_class.DocumentSource = None,
        processOption: data_class.DocumentProcessOption = None,
        client_token: str = None,
    ):
        if self.knowledge_id == None and id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"
        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=CreateDocuments", client_token=client_token
        )

        request = data_class.KnowledgeBaseCreateDocumentsRequest(
            id=id or self.knowledge_id,
            source=source,
            contentFormat=contentFormat,
            processOption=processOption,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def get_knowledge_base_list(
        self,
        knowledge_base_id: Optional[str] = None,
        maxKeys: int = 10,
        keyword: Optional[str] = None,
    ) -> data_class.KnowledgeBaseGetListResponse:
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )
        request = data_class.KnowledgeBaseGetListRequest(
            marker=knowledge_base_id or self.knowledge_id,
            maxKeys=maxKeys,
            keyword=keyword,
        )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=DescribeKnowledgeBases"
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseGetListResponse(**data)
        return resp

    def upload_documents(
        self,
        file_path: str,
        content_format: str = "rawText",
        id: Optional[str] = None,
        processOption: data_class.DocumentProcessOption = None,
        client_token: str = None,
    ):
        if not os.path.exists(file_path):
            raise FileNotFoundError("File {} does not exist".format(file_path))

        headers = self.http_client.auth_header_v2()
        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=UploadDocuments", client_token=client_token
        )

        with open(file_path, "rb") as f:
            multipart_form_data = {"file": (os.path.basename(file_path), f)}

            request = data_class.KnowledgeBaseCreateDocumentsRequest(
                id=id or self.knowledge_id,
                source=data_class.DocumentSource(type="file"),
                contentFormat=content_format,
                processOption=processOption,
            )

            data = {
                "payload": request.model_dump_json(exclude_none=True),
            }

            response = self.http_client.session.post(
                url=url,
                headers=headers,
                data=data,
                files=multipart_form_data,
            )

            self.http_client.check_response_header(response)
            self.http_client.check_console_response(response)
            data = response.json()

        return data

    def create_chunk(
        self,
        documentId: str,
        content: str,
        client_token: str = None,
    ) -> data_class.CreateChunkResponse:
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=CreateChunk", client_token=client_token
        )

        request = data_class.CreateChunkRequest(
            documentId=documentId,
            content=content,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.CreateChunkResponse(**data)
        return resp

    def modify_chunk(
        self,
        chunkId: str,
        content: str,
        enable: bool,
        client_token: str = None,
    ):
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=ModifyChunk", client_token=client_token
        )

        request = data_class.ModifyChunkRequest(
            chunkId=chunkId,
            content=content,
            enable=enable,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def delete_chunk(
        self,
        chunkId: str,
        client_token: str = None,
    ):
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=DeleteChunk", client_token=client_token
        )

        request = data_class.DeleteChunkRequest(
            chunkId=chunkId,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def describe_chunk(
        self,
        chunkId: str,
    ) -> data_class.DescribeChunkResponse:
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2("/knowledgeBase?Action=DescribeChunk")

        request = data_class.DescribeChunkRequest(
            chunkId=chunkId,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.DescribeChunkResponse(**data)
        return resp

    def describe_chunks(
        self,
        documentId: str,
        marker: str = None,
        maxKeys: int = None,
        type: str = None,
    ) -> data_class.DescribeChunksResponse:
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2("/knowledgeBase?Action=DescribeChunks")

        request = data_class.DescribeChunksRequest(
            documentId=documentId,
            marker=marker,
            maxKeys=maxKeys,
            type=type,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.DescribeChunksResponse(**data)
        return resp

    def get_all_documents(self, knowledge_base_id: Optional[str] = None) -> dict:
        """
        获取知识库中所有文档。

        Args:
            knowledge_base_id (Optional[str], optional): 知识库的ID。如果为None，则使用当前实例的knowledge_id。默认为None。

        Returns:
            dict: 包含所有文档的列表。

        Raises:
            ValueError: 如果knowledge_base_id为空，且当前实例没有已创建的knowledge_id时抛出。

        """

        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )
        knowledge_base_id = knowledge_base_id or self.knowledge_id
        doc_list = []
        response_per_time = self.get_documents_list(
            knowledge_base_id=knowledge_base_id, limit=100
        )
        list_len_per_time = len(response_per_time.data)
        if list_len_per_time != 0:
            doc_list.extend(response_per_time.data)
        while list_len_per_time == 100:
            after_id = response_per_time.data[-1].id
            response_per_time = self.get_documents_list(
                knowledge_base_id=knowledge_base_id, after=after_id, limit=100
            )
            list_len_per_time = len(response_per_time.data)
            if list_len_per_time != 0:
                doc_list.extend(response_per_time.data)

        return doc_list
